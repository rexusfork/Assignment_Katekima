from basic_lfsr import BasicLFSR
from general_lfsr import GeneralLFSR

def compare_implementations():
    # Membandingkan hasil basic dan general LFSR
    print("Comparing Basic and General LFSR implementations:")
    print("-" * 70)
    print("Iteration | Basic LFSR        | General LFSR       | Match")
    print("          | State  | Out Bit  | State  | Out Bit   |")
    print("-" * 70)
    
    basic_lfsr = BasicLFSR('0110')
    general_lfsr = GeneralLFSR(size=4, initial_state='0110', taps=[3, 0])
    
    match = True
    
    for i in range(20):
        basic_state = basic_lfsr.get_state()
        basic_bit = basic_lfsr.get_next_bit()
        
        general_state = general_lfsr.get_state()
        general_bit = general_lfsr.get_next_bit()
        
        current_match = (basic_state == general_state) and (basic_bit == general_bit)
        
        # Membandingkan antara match dan current match
        match = match and current_match
        
        print(f"{i+1:9} | {basic_state} | {basic_bit}      | {general_state} | {general_bit}      | {'Yes' if current_match else 'No'}")
    
    print("-" * 70)
    if match:
        print("SUCCESS: Both implementations produce identical outputs.")
    else:
        print("FAILURE: Implementations produce different outputs.")

if __name__ == "__main__":
    compare_implementations()