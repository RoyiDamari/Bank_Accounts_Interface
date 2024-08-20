# Notes
1. The sorting of the transaction history is done according to the time the transaction was created and not according to the time the transaction was executed, since if several transactions are carried out at the same time, then the sorting will not be relevant.
2. I pre-created in the raw data a tuple with 5 elements for a transaction to executed field, and a tuple with 6 elements for transaction history field to match the raw data structure to the excessive bonus question.
3. I created one function for options 2 and 3 so that if the user chose option 2 all transactions will be carried out regardless of the future time that the user chose, and if he chose option 3 only transactions whose future date has arrived will still be carried out.
