from MerkleTree import *
from HashFunction import *

def main():
	print('Enter your choice:')
	print('Enter 1 for Verification of data received from various Peer-to-Peer Sources')
	print('Enter 2 for performing an Audit Proof (Data Validation)')
	print('Any other key to End the program')
	choice=input()
	if(choice != '1' or choice !='2'):
		exit()
	elif(choice=='1'):
		print("Enter number of files you got from the peers: ")
		n=int(input())
		list_of_files = []
		print("Enter file names")
		for i in range(n):
			file_name = input()
			list_of_files.append(file_name)
		print("Enter Root Hash: ")
		p2pFilesVerification(root_hash,list_of_files)

	else:
		print("Building the Merkle Tree")
		print("Enter data/file for data validation(audit proof)")



if __name__ == '__main__':
	main()