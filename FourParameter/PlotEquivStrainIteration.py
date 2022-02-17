import numpy as np
import matplotlib
import matplotlib as mpl

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True

matplotlib.rcParams['text.latex.preamble'] = [
	   '\\usepackage{CJK}',
	   r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
	   r'\AtEndDocument{\end{CJK}}',
]
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
params = {
            'axes.labelsize': '16',
            'xtick.labelsize': '16',
            'ytick.labelsize': '16',
            'lines.linewidth': '1',
            'legend.fontsize': '8',
            # 'figure.figsize': '26, 24'  # set figure size
        }
pylab.rcParams.update(params)
from matplotlib import animation
from scipy import optimize
from adjustText import adjust_text
# from moviepy.editor import VideoClip
# from moviepy.video.io.bindings import mplfig_to_npimage
# import moviepy.editor as mpy

def func_A(x):
	a,b,c,d,e,f,g,h,i = 0.,-0.00610833,0.00150847,5.77749,0.77655055,0.000265084,0.00189221,0.0320232,0.520944
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))


def func_B(x):
	a,b,c,d,e,f,g,h,i = -0.0380714,-0.389742,0.832097,0.11715,1.00594,0.0430202,0.115392,-0.217208,5.14202
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))



def func_C(x):
	a,b,c,d,e,f,g,h,i = -0.000632976,-0.00186678,0.748577,5.49769,0.9,-0.0266069,0.114567,0.574344,-5.51776
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))


def func_D(x):
	a,b,c,d,e,f,g,h,i = 0.,-0.00148349,0.470459,0.0483721,0.8,0.,-0.00542422,0.0156325,4.15415   
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))

def equiv_strain(ABCD, s):
	'''根据应变值计算等效应变
	'''
	s1 = s[0]
	s2 = s[1]
	s3 = s[2]
	a = ABCD[0]
	b = ABCD[1]
	c = ABCD[2]
	d = ABCD[3]
	i1 = np.sum(s)
	j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
	fa = 1.0
	fb = -(b * np.sqrt(j2) + c * s1 + d * i1)
	fc = -a * j2
	estrain = (-fb + np.sqrt(fb ** 2 - 4 * fa * fc)) / (2 * fa)
	return estrain

def force_2_strain(e, mu, f):
	"""
	in:
		f is np.array
	out:
		epsilon is np.array
	"""
	poisson = np.array([[1, -mu, -mu],
						[-mu, 1, -mu],
						[-mu, -mu, 1]])
	strain = np.dot(poisson, f) / e
	return strain

def get_strain(beta,e,mu,ft,ct,curve):
	'''根据beta值返回应变值
	'''
	if curve == 1:
		f = np.array([ft,0,0])
		if beta <= 1.0:
			def fun(x):
				return 1.2 * x - 0.2 * x ** 6 - beta
			sol = optimize.root(fun,beta)
			x = sol.x
		elif beta > 1.0:
			def fun(x):
				return x / (2.723 * (x - 1) ** 1.7 + x) - (2.0 - beta)
			sol = optimize.root(fun,beta)
			x = sol.x
			beta = 2.0 - beta
	elif curve == 2:
		f = np.array([[0], [0], [-ft / ct]])
		if beta <= 1.0:
			def fun(x):
				return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - beta

			sol = optimize.root(fun, beta)
			x = sol.x
			beta = beta
		else:
			def fun(x):
				return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - beta)

			sol = optimize.root(fun, beta)
			x = sol.x
			beta = 2.0 - beta

	
	s = force_2_strain(e,mu,f)
	s = np.multiply(s,x)

	return s,x

def strain_stress(x):
	if x <= 1.0:
		return 1.2 * x - 0.2 * x ** 6
	else:
		return x / (2.723 * (x - 1) ** 1.7 + x)

if __name__ == "__main__":
	e = 3.14e10
	mu = 0.167
	ft = 3.47e6
	ct = 0.126
	beta = 1.0
	e0 = ft / e

	#plt.rc('text',usetex=True)
	#plt.rc('font',family='serif')

	#f = open("FourParameter\\FITABCD.data",'r')
	#lines = f.readlines()

	#x = []
	#fa = []
	#fb = []
	#fc = []
	#fd = []
	#i = 0
	#for iline in lines:
	#	i += 1
	#	if i > 1:
	#		data = list(map(float,iline.split()))
	#		x.append(data[0])
	#		fa.append(data[1])
	#		fb.append(data[2])
	#		fc.append(data[3])
	#		fd.append(data[4])
	#绘制求解过程
	# plt.figure(figsize=(4,3))
	iiter = 0
	beta = 1.2
	targetbeta = get_strain(beta,e,mu,ft,ct,1)[1]
	initstain = get_strain(beta,e,mu,ft,ct,2)[0]
	ndiv = 100

	ts = []
	plt.scatter(targetbeta,2.0 - beta)
	ts.append(plt.text(targetbeta,2.0 - beta,u"目标值", fontsize=8))
	plt.axvline(targetbeta,linewidth=0.8)
	plt.axhline(2.0 - beta,linewidth=0.8)
	#开始迭代，从beta=1.0开始
	
	beta = 1.0
	xbeta = 1.0
	
	for i in range(4):
		iiter +=1
		a = func_A(xbeta)
		b = func_B(xbeta)
		c = func_C(xbeta)
		d = func_D(xbeta)
		abcd = np.array([a,b,c,d])
		es = []
		y = []

		for idiv in range(ndiv):
			beta = 0.5 * idiv / ndiv + 1.0   #1.0-1.5范围内的x
			s = get_strain(beta,e,mu,ft,ct,2)[0]
			es.append(equiv_strain(abcd,s) / e0)
			y.append(2.0 - beta)
		plt.plot(es,y,"-.",linewidth=0.5,label=r"$\beta={0:.3f}$,迭代$={1:2d}$".format(float(strain_stress(xbeta)),iiter))

		es = equiv_strain(abcd,initstain) / e0
		plt.axvline(es,linestyle='-.',linewidth=0.5)
		ts.append(plt.text(es,0.8,r"$\beta={0:.3f}$,迭代$={1:2d}$".format(float(strain_stress(xbeta)),iiter), fontsize=8))
		# plt.annotate(r'$\beta={0:.3f},iteration={1:2d}$'.format(float(xbeta),iiter),xy=(es,0.8),xytext=(es,0.8),textcoords='offset points')
		xbeta = es

	adjust_text(ts,arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.01', color='blue'))
	plt.xlabel(r'$\varepsilon^*/\varepsilon_0$', fontsize=8)
	plt.ylabel(r'$\sigma^*/f_t$', fontsize=10)
	# plt.legend()
	plt.xlim(1.0,1.8)
	plt.ylim(0.7,0.9)
	plt.tight_layout()
	# plt.show()
	plt.legend()
	plt.savefig("FourParameter\\Figs\\EquivStrainIteration.pdf")
	
	#plt.show()
	plt.close()


	