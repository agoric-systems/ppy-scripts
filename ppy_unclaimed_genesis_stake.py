import json

TOTAL_PPY_SUPPLY = 5503920

genesis_data = json.load(open('genesis.json'))

crowdsale_and_vesting_balances = genesis_data["initial_balances"] + genesis_data["initial_vesting_balances"]

print("Total number of crowdsale and vesting balances in genesis:\n %s" % len(crowdsale_and_vesting_balances))

claims_data = json.load(open('claims.json'))

print("Total number of balance claims processed as of January 10, 2018:\n %s" % len(claims_data))
print("Total unclaimed crowdsale and vesting genesis balances remaining:\n %s" % (len(crowdsale_and_vesting_balances) - len(claims_data)))

unclaimed_crowdsale_genesis_entries = crowdsale_and_vesting_balances.copy()
total_stake_claimed = 0
for claim in claims_data:
    genesis_index = int(claim["balance_to_claim"].split(".")[2])
    if genesis_index <= len(crowdsale_and_vesting_balances):
        amount = claim['total_claimed'].get('amount')
        # apparently the amount field has an additional nested key for large amounts
        if type(amount) is dict:
            amount = amount['$numberLong']
        total_stake_claimed += int(amount)
        unclaimed_crowdsale_genesis_entries[genesis_index] = None
    else:
        print(claim)


total_unclaimed_stake = 0
remaining_unclaimed_genesis_entries = ""
for genesis_entry in unclaimed_crowdsale_genesis_entries:
    # skip claimed entries
    if genesis_entry is None:
        continue
    normalized_amount = int(genesis_entry['amount']) / 100000
    remaining_unclaimed_genesis_entries += ("%s | %s PPY\n" % (genesis_entry['owner'], normalized_amount))
    total_unclaimed_stake += int(amount)

normalized_total_stake_claimed = total_stake_claimed / 100000
normalized_total_stake_unclaimed = total_unclaimed_stake / 100000

print("Total claimed crowdsale and vesting stake:\n %s PPY" % normalized_total_stake_claimed)
print("Total claimed crowdsale and vesting stake as percentage of \ntotal supply:\n %s" % ((normalized_total_stake_claimed / TOTAL_PPY_SUPPLY) * 100) + " %")
print("Total unclaimed crowdsale and vesting stake:\n %s PPY" % normalized_total_stake_unclaimed)
print("Total unclaimed crowdsale stake as percentage of total supply:\n %s" % ((normalized_total_stake_unclaimed / TOTAL_PPY_SUPPLY) * 100) + " %")
print("Known unclaimed genesis owner / balances")
print("========================================")
print(remaining_unclaimed_genesis_entries)
