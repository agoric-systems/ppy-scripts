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
unclaimed_crowdsale_stake = 0
unclaimed_vesting_stake = 0
remaining_unclaimed_genesis_entries = ""
last_crowdsale_index = len(genesis_data["initial_balances"]) - 1
for index, genesis_entry in enumerate(unclaimed_crowdsale_genesis_entries):
    # skip claimed entries
    if genesis_entry is None:
        continue
    normalized_amount = int(genesis_entry['amount']) / 100000
    remaining_unclaimed_genesis_entries += ("%s | %s PPY\n" % (genesis_entry['owner'], normalized_amount))
    total_unclaimed_stake += int(genesis_entry['amount'])
    if index <= last_crowdsale_index:
        unclaimed_crowdsale_stake += int(genesis_entry['amount'])
    else:
        unclaimed_vesting_stake += int(genesis_entry['amount'])


normalized_total_stake_claimed = total_stake_claimed / 100000
normalized_total_stake_unclaimed = total_unclaimed_stake / 100000
normalized_unclaimed_crowdsale_stake = unclaimed_crowdsale_stake / 100000
normalized_unclaimed_vesting_stake = unclaimed_vesting_stake / 100000


print("Total claimed crowdsale and vesting stake:\n %s PPY" % normalized_total_stake_claimed)
print("Total claimed crowdsale and vesting stake as percentage of \ntotal supply:\n %s" % ((normalized_total_stake_claimed / TOTAL_PPY_SUPPLY) * 100) + " %")
print("Unclaimed crowdsale stake:\n %s PPY" % normalized_unclaimed_crowdsale_stake)
print("Unclaimed crowdsale stake as percentage of total supply:\n %s" % ((normalized_unclaimed_crowdsale_stake / TOTAL_PPY_SUPPLY) * 100) + " %")
print("Unclaimed vesting stake:\n %s PPY" % normalized_unclaimed_vesting_stake)
print("Unclaimed vesting stake as percentage of total supply:\n %s" % ((normalized_unclaimed_vesting_stake / TOTAL_PPY_SUPPLY) * 100) + " %")
print("Total unclaimed crowdsale and vesting stake:\n %s PPY" % normalized_total_stake_unclaimed)
print("Total unclaimed crowdsale and vesting stake as percentage of total supply:\n %s" % ((normalized_total_stake_unclaimed / TOTAL_PPY_SUPPLY) * 100) + " %")
print("Known unclaimed genesis owner / balances")
print("========================================")
print(remaining_unclaimed_genesis_entries)
