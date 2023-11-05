import numpy as np
class Unit:
	s:int
	m:int
	kg:int
	a:int
	def __init__(self,kg:int,m:int,s:int,a:int,/,pretty_print:bool=False):
		self.kg=kg
		self.m=m
		self.s=s
		self.a=a
		self.pprint=pretty_print
	def __hash__(self) -> int:
		# 13,17,23,29
		temp=0
		temp+=(13*self.kg)
		temp+=(17*self.m)
		temp+=(23*self.s)
		temp+=(29>self.a)
		return temp
	def __truediv__(self,val:'Unit') -> 'Unit':
		res=self
		_sub=lambda a,b: a-b if a !=0 else 0
		res=Unit(
				self.kg-val.kg,
				self.m-val.m,
				self.s-val.s,
				self.a-val.a
				)
		return res

	def __mul__(self,val:'Unit') -> 'Unit':
		res=self
		res=Unit(
				self.kg+val.kg,
				self.m+val.m,
				self.s+val.s,
				self.a+val.a
				)
		return res
	def __pow__(self,val:int) -> 'Unit':
		_add=lambda a,b: a*b
		# _add=lambda a,b: a+b-1 if a != 0 else 0
		res=Unit(
				_add(self.kg,val),
				_add(self.m,val),
				_add(self.s,val),
				_add(self.a,val)
				)
		return res

	def __repr__(self) -> str:
		if self.pprint:
			return self.pretty()
		else:
			return self.plain_print()
	
	def pretty(self):
		u=self
		knowns=get_known_units()
		inv={v:k for k,v in knowns.items()}
		name=inv[self]
		del knowns[name]
		mat=to_mat(knowns)
		res={}
		while u != 0:
			deltas=np.sum((abs(u.v)-abs(mat)),axis=1)
			closest_idx=np.where(abs(deltas)==min(abs(deltas)))[0][0] #pyright:ignore
			closest_name=list(knowns.keys())[closest_idx]
			closest=knowns[closest_name]
			num=deltas[closest_idx]
			res[closest_name]=num
			# print(f"closest found was {closest_name}")
			# print(f'{u=}')
			# print(f'{closest_name}={closest}')
			u=u/(closest**(num))
		def rep(unit,pow):
			if pow==1:
				return str(unit)+ ' '
			elif pow != 0:
				return f'{unit}^{pow} '
			else:
				return ''
		return ''.join([rep(k,v) for k,v in res.items()])

	def plain_print(self):
		def rep(pow,unit):
			if pow==1:
				return str(unit)+ ' '
			elif pow != 0:
				return f'{unit}^{pow} '
			else:
				return ''
		_acc=''
		_acc+=rep(self.kg,'kg')
		_acc+=rep(self.m,'m')
		_acc+=rep(self.s,'s')
		_acc+=rep(self.a,'A')
		if _acc=='':
			_acc="(unitless)"
		return _acc
	def __eq__(self, rhs) -> bool:
		if isinstance(rhs,int):
			return sum(self.v)==rhs
		return False
	@property
	def v(self):
		return np.array(((self.kg,self.m,self.s,self.a))).T
def reduce(u:Unit) -> str:
	knowns=get_known_units()
	mat=to_mat()
	res={}
	while u != 0:
		deltas=np.sum(abs(mat-u.v),axis=1)
		closest_idx=np.where(abs(deltas)==min(abs(deltas)))[0][0] #pyright:ignore
		closest_name=list(knowns.keys())[closest_idx]
		closest=knowns[closest_name]
		if deltas[closest_idx]==0:
			deltas[closest_idx]=1
		res[closest_name]=deltas[closest_idx] #pyright:ignore
		# print(f"closest found was {closest_name}")
		# print(f'{u=}')
		# print(f'{closest_name}={closest}')
		u=u/closest
	def rep(unit,pow):
		if pow==1:
			return str(unit)+ ' '
		elif pow != 0:
			return f'{unit}^{pow} '
		else:
			return ''
	return ''.join([rep(k,v) for k,v in res.items()])
def to_mat(d:dict|None=None) -> np.ndarray:
	if d==None:
		return np.array([k.v for k in get_known_units().values()])
	return np.array([k.v for k in d.values()])
def get_known_units() -> dict[str,Unit]:
	return {k:v for k,v in globals().items() if isinstance(v,Unit)}


kg=Unit(1,0,0,0)
m=Unit(0,1,0,0)
s=Unit(0,0,1,0)
A=Unit(0,0,0,1)
V=kg*(m**2)*(s**-3)*(A**-1)
J=kg*(m**2)*(s**-2)
N=kg*m/(s**2)
C=A*s
W=kg*(m**2)*(s**-3)
F=(kg**-1)*(m**-2)*(s**4)*(A**2)
hash(F)
print(F.pretty())
#if __name__=="__main__":
if __name__=="_no":
	p=input(">>")
	while p!= 'q':
		try:
			print(eval(p))
		except:
			out=exec(p)
			if out != None:
				print(out)
		p=input(">>")
