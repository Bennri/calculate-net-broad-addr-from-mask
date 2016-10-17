# calculator for classful networks
# which means total bits are 8 => T_b = 8

# using subnetmask: 255.255.255.X for class C networks
tb = 8
mask_bits_dict= {
	0: 0,
	128: 1,
	192: 2,
	224: 3,
	240: 4,
	248: 5,
	252: 6,
	254: 7,
	255: 8
}

def get_number_of_bits_for_subnetting(subnetmask):
	value_list = subnetmask.split('.')
	try:
		v = int(value_list[-1])
		if 0 <= v <= 255 and v in mask_bits_dict:
			n = mask_bits_dict[v]
			# number of bits used for subnetting
			return n
		else:
			raise ValueError("Not a proper value!")
	except TypeError, e:
		raise e

def get_number_of_bits_left_for_host(T_b, n):
	m = T_b - n
	return m


def get_number_of_subnets(n):
	return pow(2,n)

def get_value_last_bit_used_for_sub_mask(m):
	delta = pow(2,m)
	return delta
def get_number_of_hosts_per_subnet(m):
	amount_hosts = pow(2,m)-2
	return amount_hosts

def get_corresponding_subnet(ip_address, mask, n, m, subs, delta, amount_hosts):
	host = int(ip_address.split('.')[-1])
	network_address = 0
	broadcast_address = 0
	subnet_range_of_host = []
	i = 0
	while i < 256:
		network_address = i
		# i = i + amount_hosts + 1
		# e.g. i = 0,
		# add value of last bit for subnet masking which is e.g 32, which means
		# xyz.xyz.xyz.0 will be the network address, 
		# xyz.xyz.xyz.31 will be the broadcast address
		# which is altogether 32 which includes broadcast and network address
		i = i + delta - 1
		broadcast_address = i

		if network_address < host < broadcast_address:
			subnet_range_of_host.append(network_address)
			subnet_range_of_host.append(broadcast_address)
		i = i + 1
	return subnet_range_of_host


# if you have given an ip address and the corresponding subnet mask, you can use this method to calculate the subnet
# of your given ip address
def calculate_subnet_from_ip_and_mask(ip_address, mask):
	"""
	ip address and subnet mask given, calculate the subnet in which the ip address
	appears
	"""
	n = get_number_of_bits_for_subnetting(mask)
	m = get_number_of_bits_left_for_host(tb, n)
	subs = get_number_of_subnets(n)
	delta = get_value_last_bit_used_for_sub_mask(m)
	h = get_number_of_hosts_per_subnet(m)
	r = get_corresponding_subnet(ip_address, mask, n, m, subs, delta, h)
	return r



# helper: calculate subnet mask from ip and network address

def address_to_bin(address):
	address_list_dec = address.split('.')
	if len(address_list_dec) == 4:
		try:
			address_list_bin_str = []
			for a in address_list_dec:
				b = bin(int(a)).split('b')[-1]
				# python: (42) -> '0b101010', but we need 8 bit which means '00101010'
				# this is done by the following if statement
				if len(b) < 8:
					diff = 8 - len(b)
					b = '0' * diff + b
				address_list_bin_str.append(b)

			return address_list_bin_str
		except TypeError, e:
			raise e
	else:
		raise ValueError("Not a valid 32 bit IPv4 address!")


def calc_subnet_mask_from_bin_addresses_return_bin_class_C(ip_address, network_address):
	"""
	Given two ip addresses represented as ['11111111', '00101010', '11111111', '00101010']
	we will calculate the subnet mask of the used IP address by using 'not XOR'
	keep in mind that we are calculating it for a class C network
	"""
	if len(ip_address) == 4 and len(network_address) == 4:
		subnet_mask = ['11111111', '11111111', '11111111']  # 255.255.255.X
		block8bit_ip = ip_address[-1]
		block8bit_net = network_address[-1]
		block8bit_xor = ""
		for i in range(len(block8bit_ip)):
			if block8bit_ip[i] == block8bit_net[i]:
				block8bit_xor += '1'
			else:
				break
		curr_len = len(block8bit_xor)
		diff = 8 - curr_len
		block8bit_xor = block8bit_xor + '0' * diff  # X
		subnet_mask.append(block8bit_xor)  # append X -> ['11111111', '11111111', '11111111', 'bbbbbbbb']
		return subnet_mask

	else:
		raise ValueError("IP addresses do not have the same size! Shall be 4 blocks each with 8 bit.")


def bin_address_to_dec(bin_address):
	if len(bin_address) == 4:
		dec_address = []
		for block in bin_address:
			#print block
			dec = int(block, 2)
			dec_address.append(dec)
		return dec_address
	else:
		raise ValueError("IPv4 addresses have 4 blocks each with 8 bit.")


def bin_subnetmask_to_dec(bin_net_mask):
	block = bin_net_mask[-1]
	dec = int(block, 2)
	pass
# ip_address = "210.1.1.100"
# mask = "255.255.255.224"
# calculate_subnet_from_ip_and_mask(ip_address, mask)
# address_to_bin("255.255.248.0")


def calc_subnet_mask_from_ip_and_network_address_dec(ip_address, network_address):
	"""
	IP address and network address given in decimal representation
	"""
	ip_bin = address_to_bin(ip_address)
	net_bin = address_to_bin(network_address)
	subnet_mask_bin = calc_subnet_mask_from_bin_addresses_return_bin_class_C(ip_bin, net_bin)
	dec_subnet_mask = bin_address_to_dec(subnet_mask_bin)
	return dec_subnet_mask


# test for given IP address and network address
ip="192.168.100.172"
net="192.168.100.160"
subnet_mask = calc_subnet_mask_from_ip_and_network_address_dec(ip, net)
print ("Subnet mask: %s" % subnet_mask)
