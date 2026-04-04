import csv
import sys
import requests
import time

API_URL = "http://localhost:8000/api/v1/etch_deed"
API_KEY = "PQ_LIVE_DEMO_SECRET"

def run_bulk_upload(csv_file):
    print(f"═══ ProtoQol BULK_ETCH (Excel-Killer) ═══")
    print(f"Targeting: {API_URL}")
    print(f"File: {csv_file}")
    print("-" * 40)

    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                desc = row.get('description')
                mission = row.get('mission_id', 'eco_asar')
                nomad = row.get('nomad_id', 'Anonymous')
                source = row.get('source', 'API Gateway')

                print(f"\n[ENTRY {count+1}] Submitting from {source}: {desc[:40]}...")
                
                start = time.time()
                try:
                    resp = requests.post(API_URL, data={
                        "description": desc,
                        "mission_id": mission,
                        "nomad_id": nomad,
                        "source": source
                    }, headers={"X-API-Key": API_KEY}, timeout=30)
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        verdict = data.get('verdict')
                        tx = data.get('tx_hash', 'N/A')
                        print(f"  Outcome: {verdict} | TX: {tx[:24]}... | ({time.time()-start:.1f}s)")
                    else:
                        print(f"  Failed: HTTP {resp.status_code} | {resp.text}")
                except Exception as e:
                    print(f"  Request Error: {e}")
                
                count += 1
                # Small sleep to prevent network congestion
                time.sleep(1)

            print(f"\n═══ Processed {count} entries into Solana Ledger ═══")

    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Create a sample CSV if none provided for testing
        print("Usage: python bulk_etch.py <file.csv>")
        print("Usage: Creating sample_deeds.csv for you...")
        with open("sample_deeds.csv", "w", encoding='utf-8') as f:
            f.write("mission_id,description,nomad_id\n")
            f.write("elders_aktobe,\"Помог бабушке перейти дорогу и донести сумки\",nomad_1\n")
            f.write("eco_asar,\"Собрал мешок пластика на пляже\",nomad_2\n")
            f.write("it_mentorship,\"I am lying, I did nothing today\",nomad_3\n")
        print("Done. Run: python bulk_etch.py sample_deeds.csv")
    else:
        run_bulk_upload(sys.argv[1])
