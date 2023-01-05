import java.math.BigInteger;

public class Rational {
	long num;
	long denom;
	
	public Rational(long num, long denom)
	{
		this.num = num;
		this.denom = denom;
		reduce();
	}
	
	private void reduce()
	{
		long gcd = gcd(num, denom);
		num /= gcd;
		denom /= gcd;
	}
	
	public Rational add(Rational r)
	{
		return new Rational(num*r.denom + r.num * denom, denom*r.denom);
	}
	
	public Rational multiply(Rational r)
	{
		return new Rational(num*r.num,denom*r.denom);
	}
	
	public boolean equals(Rational r)
	{
		return r.num == num && r.denom == denom;
	}
	
	public boolean equals(long i)
	{
		return num == i && denom == 1;
	}
	
	public long gcd(long a, long b)
	{
		return BigInteger.valueOf(a).gcd(BigInteger.valueOf(b)).longValue();
	}
	
	public boolean lessThan(double d)
	{
		return (num+0.0) / denom < d;
	}
	
	public String toString()
	{
		return toDoubleString();//num+"/"+denom;
	}
	
	public String toDoubleString()
	{
		return (num+0.0)/denom+"";
	}
}
