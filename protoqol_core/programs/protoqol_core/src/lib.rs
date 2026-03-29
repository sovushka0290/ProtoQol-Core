use anchor_lang::prelude::*;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

// Oracle Master Biy —The only authorized signer for ProtoQol truth etching
const ORACLE_MASTER_AUTHORITY: &str = "98EJYhcrJHWYsdRvTg5Tg2zi47midrFHBhdsrdnoLezh";

#[program]
pub mod protoqol_core {
    use super::*;

    pub fn etch_deed(
        ctx: Context<EtchDeed>, 
        nomad_id: Pubkey,
        deed_id: String, 
        mission_id: String, 
        impact_points: u64, 
        verdict: String,
        integrity_hash: String
    ) -> Result<()> {
        let deed = &mut ctx.accounts.deed_record;

        // Данные кристаллизуются On-Chain
        deed.nomad = nomad_id.key();
        deed.oracle = ctx.accounts.oracle.key();
        deed.mission_id = mission_id;
        deed.impact_points = impact_points;
        deed.verdict = verdict;
        deed.integrity_hash = integrity_hash;
        deed.timestamp = Clock::get()?.unix_timestamp;

        // Обновление глобального рейтинга репутации (PDA)
        let profile = &mut ctx.accounts.nomad_profile;
        if profile.nomad == Pubkey::default() {
            profile.nomad = nomad_id.key();
        }
        profile.total_impact = profile.total_impact.checked_add(impact_points).unwrap_or(u64::MAX);

        msg!("ProtoQol Deed Etched: {}", deed_id);
        msg!("Biy Oracle Signature Verified. Gas Sponsored by Foundation.");
        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(nomad_id: Pubkey, deed_id: String)]
pub struct EtchDeed<'info> {
    #[account(
        init,
        seeds = [b"deed", nomad_id.as_ref(), deed_id.as_bytes()],
        bump,
        payer = oracle,
        space = 8 + DeedRecord::INIT_SPACE
    )]
    pub deed_record: Account<'info, DeedRecord>,

    #[account(
        init_if_needed,
        seeds = [b"profile", nomad_id.as_ref()],
        bump,
        payer = oracle,
        space = 8 + NomadProfile::INIT_SPACE
    )]
    pub nomad_profile: Account<'info, NomadProfile>,

    // [SECURITY FIX] Only the Master Biy Oracle can sign and pay for truth etching.
    // Unauthorized callers (even if they pay) will be rejected.
    #[account(
        mut,
        constraint = oracle.key().to_string() == ORACLE_MASTER_AUTHORITY @ ErrorCode::UnauthorizedOracle
    )]
    pub oracle: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[account]
#[derive(InitSpace)]
pub struct DeedRecord {
    pub nomad: Pubkey,
    pub oracle: Pubkey,
    #[max_len(32)]
    pub mission_id: String,
    pub impact_points: u64,
    #[max_len(16)]
    pub verdict: String,
    #[max_len(64)]
    pub integrity_hash: String,
    pub timestamp: i64,
}

#[account]
#[derive(InitSpace)]
pub struct NomadProfile {
    pub nomad: Pubkey,
    pub total_impact: u64,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Only the designated Master Biy Oracle can signature truth on-chain.")]
    UnauthorizedOracle,
}

