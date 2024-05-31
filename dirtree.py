import os
import argparse

def get_dirtree(root, max_depth):
    """utility for creating string representation for the 'dirtree' tex-package.
    input:
        root(str): path to desired root directory
        max_depth(int): max directory nesting to consider
    returns:
        dirtree(str): dirtree representation ready for copy-paste to tex
    todos:
        escape tex special characters before final return
        make shell args type-safe
    """
    def _flatten(container):
        '''flatten arbitrarily often nested lists. source from: https://stackoverflow.com/a/10824420 '''
        for i in container:
            if isinstance(i, (list,tuple)):
                for j in _flatten(i):
                    yield j
            else:
                yield i

    def _rec_dirtree(root, n, max_depth):
        name = root.split(os.sep)[-1]
        node = f'.{n} {name}.\n'
        if max_depth != -1:
            if n >= max_depth:
                return node
        if not os.path.isdir(root):
            return node
        
        children = [os.path.join(root, c) for c in os.listdir(root)]
        nodes = [node]
        for c in children:
            nodes.append(_rec_dirtree(c, n+1, max_depth))
        return nodes

    nodes = _rec_dirtree(root, 1, max_depth)
    dirtree = ''.join([x for x in _flatten(nodes)])
    return dirtree

parser = argparse.ArgumentParser()
parser.add_argument('root_dir')
parser.add_argument('max_depth', help='specify how many layers deep to list. -1 disable depth restriction.')
parser.add_argument('out_file')
parser.add_argument('-v', '--verbose', action='store_true')  
args = parser.parse_args()

if os.path.exists(args.out_file):
    raise ValueError('The specified output-file already exists')

if args.verbose:
    print(args)

dirtree = get_dirtree(args.root_dir, int(args.max_depth))
if args.verbose:
    print(dirtree)

with open(args.out_file, 'w') as fp:
    fp.write(dirtree)
        