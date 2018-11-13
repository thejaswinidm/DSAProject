import math
 
rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
 
constants = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
 
init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]



#functions is a list of 64 functions 
functions = 16*[lambda b, c, d: (b & c) | (~b & d)] + \
            16*[lambda b, c, d: (d & b) | (~d & c)] + \
            16*[lambda b, c, d: b ^ c ^ d] + \
            16*[lambda b, c, d: c ^ (b | ~d)]



 #index_functions is a list of 64 functions
index_functions = 16*[lambda i: i] + \
                  16*[lambda i: (5*i + 1)%16] + \
                  16*[lambda i: (3*i + 5)%16] + \
                  16*[lambda i: (7*i)%16]
 


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF
 


def hash_fun(message):
    #message is broken into chunks of 512 bits
    message = bytearray(message) #copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)

    
    while len(message)%64 != 56:    #appending zeroes till number of bits in message is 64 less than multiple of 512
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little') #appending original length in 64 bits to make length of message a multiple of 512 
 
    hash_pieces = init_values[:]
 
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst+64]


        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c


        for i, val in enumerate([a, b, c, d]):     
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF
 
    return sum(x<<(32*i) for i, x in enumerate(hash_pieces))
 

#converting sum to hexadecimal representation(string)
def hash_fun_hex_str(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

def hash_update(temp1,temp):
    fi_temp=temp1+temp
    fi_temp_bytes=bytes(fi_temp,"utf-8")
    fi_temp_hash_str=hash_fun_hex_str(hash_fun(fi_temp_bytes))
    return fi_temp_hash_str