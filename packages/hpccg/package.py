##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Hpccg(MakefilePackage):
    """Intended to be the 'best approximation to an unstructured implicit
    finite element or finite volume application in 800 lines or fewer.'"""

    homepage = "https://mantevo.org/about/applications/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/HPCCG/HPCCG-1.0.tar.gz"

    version('1.0', '2e99da1a89de5ef0844da5e6ffbf39dc')

    variant('mpi', default=False, description='Build with MPI support')
    variant('openmp', default=False, description='Build with OpenMP support')

    # Optional dependencies
    depends_on('mpi', when= '+mpi')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('CXX=.*', 'CXX=c++')
        makefile.filter('LINKER=.*', 'LINKER=c++')

        if '%gcc' not in self.spec:
            makefile.filter('CPP_OPT_FLAGS = -O3 -ftree-vectorize -ftree-vectorizer-verbose=2', '#')


        if '+mpi' in self.spec:
            makefile.filter('USE_MPI =', 'USE_MPI = -DUSING_MPI')
            makefile.filter('CXX=.*', 'CXX={}'.format(spec['mpi'].mpicxx))
            makefile.filter('LINKER=.*', 'LINKER={}'.format(spec['mpi'].mpicxx))

        if '+openmp' in self.spec:
            makefile.filter('USE_OMP =', 'USE_OMP = -DUSING_OMP')
            makefile.filter('#OMP_FLAGS = -fopenmp', 'OMP_FLAGS = {}'.format(self.compiler.openmp_flag))

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        install('test_HPCCG', prefix.bin)
