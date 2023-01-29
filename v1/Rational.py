class Rational:

	def __init__(self,numerator, denominator):
		self.num = numerator
		self.denom = denominator
		self.reduce()

	def reduce(self):
		gcd = gcd(num, denom)
		self.num //= gcd
		self.denom //= gcd

	def add(self, r):
		return Rational(self.num*r.denom + r.num * self.denom, self.denom*r.denom)

	def multiply(self, r):
		return Rational(self.num*r.num,self.denom*r.denom);

	def equals(self, r):
		return r.num == self.num and r.denom == self.denom;

	def equals(self, i):
		return self.num == i and self.denom == 1

	def gcd(self, x, y):
    	while(y):
           x, y = y, x % y
        return abs(x)

	def lessThan(self, d):
		return (self.num+0.0) / self.denom < d

	def __str__(self):
		return self.toDoubleString()

	def toDoubleString(self):
		return (num+0.0)/denom+"";
