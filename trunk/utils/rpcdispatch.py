from django.conf import settings

class Dispatcher:
	"""
	This class encapsulates a dispatcher. This is used to build
	the real table needed for the RPC method dispatch. An instance
	of this class is returned by the dispatch and include functions.
	"""
	def __init__(self, base, module=None, entries=None):
		self.dispatch = {}
		if module is None and entries is None:
			raise ValueError('either module or entries needs to be specified')
		if entries is None:
			module = __import__(module, '', '', [''])
			self.dispatch.update(module.rpccalls.dispatch)
		else:
			for el in entries:
				if type(el) == tuple:
					(fn, fc) = el
					if base: fc = '%s.%s' % (base, fc)
					p = fc.rfind('.')
					modname = fc[:p]
					funcname = fc[p+1:]
					self.dispatch[fn] = getattr(__import__(modname, '', '', ['']), funcname)
				elif isinstance(el, Dispatcher):
					self.dispatch.update(el.dispatch)

	def find(self, function):
		"""
		This method searches for a matching function definition.
		"""
		return self.dispatch.get(function, None)

def dispatch(base, *entries):
	return Dispatcher(base, entries=entries)

def include(module):
	return Dispatcher('', module=module)

dispatch_table = None

def dispatcher():
	global dispatch_table
	if dispatch_table is None:
		dispatch_table = include(settings.ROOT_RPCCONF)
	return dispatch_table

if __name__ == '__main__':
	print dispatcher().dispatch
