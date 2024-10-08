import sys
import re

def make_member_dict(member):
	m = {0: 0, 1: 0, 2: 0}
	for e in member:
		e = e.split('*')
		if len(e) == 1 and 'X' in e[0]:
			if '^' not in e[0]:
				e[0] += '^1'
			num = 1
			if e[0][0] == '-':
				num = -1
				e[0] = e[0][1:]
			if int(e[0][2:]) not in m.keys():
				m[int(e[0][2:])] = num
			else:
				m[int(e[0][2:])] += num
		elif len(e) == 1 or e[1] == 'X^0':
			m[0] += float(e[0])
		elif len(e) == 2 and (e[1] == 'X' or e[1] == 'X^1'):
			m[1] += float(e[0])
		elif len(e) == 2:
			if int(e[1][2:]) not in m.keys():
				m[int(e[1][2:])] = float(e[0])
			else:
				m[int(e[1][2:])] += float(e[0])
		else:
			print('bad input?', file=sys.stderr)
	return m


def reduce_equation(left, right):
	left_keys = left.keys()
	right_keys = right.keys()

	exp1 = set(left_keys)
	exp2 = set(right_keys)
	union = list(exp1.union(exp2))

	for e in union:
		if e not in left_keys:
			left[e] = right[e] * -1
		elif e not in right_keys:
			pass
		else:
			left[e] -= right[e]
	return left


def parse(equation):
	equation = equation.upper()
	if '=' not in equation:
		print("that is not an equation")
		exit()

	try:
		splitted = equation.split('=')
		if splitted[1] == '':
			exit()
		splitted[0] = splitted[0].replace('-', ';-')
		splitted[1] = splitted[1].replace('-', ';-')
		splitted[0] = re.split('\+|;', splitted[0])
		splitted[1] = re.split('\+|;', splitted[1])

		if splitted[0][0] == '':
			splitted[0] = splitted[0][1:]
		if splitted[1][0] == '':
			splitted[1] = splitted[1][1:]

		left = make_member_dict(splitted[0])
		right = make_member_dict(splitted[1])

		return reduce_equation(left, right)
	except:
		print("There seemed to be a problem with your equation, make sure everything is well written")
		exit()


def show_equation(equation):
	keys = list(equation.keys())
	keys.sort()
	string = ''

	for k in keys:
		num = equation[k]
		if num == 0:
			continue
		if string == '':
			string += f'{num} * X^{k} '
		else:
			if num > 0:
				string += f'+ {num} * X^{k} '
			else:
				string += f'- {abs(num)} * X^{k} '
	if string == '':
		string = '0 '
	string += '= 0'
	print(f'Reduced form: {string}')


def get_degree(equation):
	keys = list(equation.keys())
	keys.sort(reverse=True)

	for k in keys:
		if equation[k] != 0:
			print(f'Polynomial degree: {k}')
			return k
	print ('Nice Try, the right side cancels the left side so any real number works', file=sys.stderr)
	exit()


def solve_second_degree(equation):
	disc = equation[1]**2 - 4 * equation[0] * equation[2]

	if disc > 0:
		#2 solutions
		disc = disc**(1/2)
		x1 = round((-equation[1] + disc)/(2*equation[2]), 3)
		x2 = round((-equation[1] - disc)/(2*equation[2]), 3)
		print('Discriminant is strictly positive, the two solutions are:', x1, x2, sep='\n')
	elif disc == 0:
		x = round(-equation[1] / (2*equation[2]), 3)
		print('Discriminant is 0, therefore there is a single solution:', x, sep = '\n')
	else:
		disc = abs(disc)**(1/2)
		real = round(-equation[1] / (2*equation[2]), 3)
		imaginary = round(abs(disc / (2*equation[2])), 3)
		print('Discriminant is strictly negative, the solutions are imaginary:')
		print(f'{real} + {imaginary}*i')
		print(f'{real} - {imaginary}*i')


if __name__ =='__main__':
	if (len(sys.argv) != 2):
		print('wrong number of arguments', file = sys.stderr)
		exit()

	equation = sys.argv[1].replace(" ", "")
	accepted = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+', '*', 'X', '^', '.', '=']
	for c in equation:
		if str(c) not in accepted:
			print (f"you used some illegal characters here: {c}")
			exit()

	equation = parse(equation)
	show_equation(equation)
	degree = get_degree(equation)
	if degree > 2:
		print('The polynomial degree is strictly greater than 2, I can\'t solve.')
		exit()
	if degree == 1:
		print(f'The solution is: {round((equation[0] * -1) / equation[1], 3)}')
		exit()
	if degree == 2:
		solve_second_degree(equation)
		exit()
	if degree == 0:
		print('Not even a magician would get you an answer')
		exit()
