include Makefile.dependencies

SHELL = /bin/bash

CC = gcc

CFLAGS = -I../headers -O2 -fomit-frame-pointer

DEPFLAG = -MM

INCLUDE = Dirichlet.h \
	  SnapPea.h \
	  canonize.h \
	  covers.h \
	  dual_one_skeleton_curve.h \
	  isometry.h \
	  kernel.h \
	  kernel_prototypes.h \
	  kernel_typedefs.h \
	  link_projection.h \
	  normal_surfaces.h \
	  positioned_tet.h \
	  symmetry_group.h \
	  tables.h \
	  terse_triangulation.h \
	  tersest_triangulation.h \
	  triangulation.h \
	  triangulation_io.h \
	  unix_cusped_census.h \
	  winged_edge.h

OBJS =    Dehn_coefficients.o \
	  Dirichlet.o \
	  Dirichlet_basepoint.o \
	  Dirichlet_construction.o \
	  Dirichlet_extras.o \
	  Dirichlet_precision.o \
	  Dirichlet_rotate.o \
	  Moebius_transformations.o \
	  abelian_group.o \
	  canonize.o \
	  canonize_part_1.o \
	  canonize_part_2.o \
	  canonize_result.o \
	  change_peripheral_curves.o \
	  chern_simons.o \
	  choose_generators.o \
	  close_cusps.o \
	  complex.o \
	  complex_length.o \
	  continued_fractions.o \
	  core_geodesics.o \
	  cover.o \
	  current_curve_basis.o \
	  cusp_cross_sections.o \
	  cusp_neighborhoods.o \
	  cusp_shapes.o \
	  cusps.o \
          decode_new_DT.o \
	  direct_product.o \
	  double_cover.o \
	  drilling.o \
	  dual_curves.o \
	  edge_classes.o \
	  elements_generate_group.o \
	  filling.o \
	  find_cusp.o \
	  finite_vertices.o \
	  fundamental_group.o \
	  gcd.o \
	  gluing_equations.o \
	  holonomy.o \
	  homology.o \
	  hyperbolic_structure.o \
	  identify_solution_type.o \
	  index_to_hue.o \
	  interface.o \
	  intersection_numbers.o \
	  isometry.o \
	  isometry_closed.o \
	  isometry_cusped.o \
	  length_spectrum.o \
	  link_complement.o \
	  matrix_conversion.o \
	  matrix_generators.o \
	  my_malloc.o \
	  normal_surface_construction.o \
	  normal_surface_recognition.o \
	  normal_surface_splitting.o \
	  o31_matrices.o \
	  orient.o \
	  peripheral_curves.o \
	  polyhedral_group.o \
	  positioned_tet.o \
	  precision.o \
	  punctured_torus_bundles.o \
	  rehydrate_census.o \
	  representations.o \
	  shingling.o \
	  shortest_cusp_basis.o \
	  simplify_triangulation.o \
	  sl2c_matrices.o \
	  solve_equations.o \
	  subdivide.o \
	  symmetric_group.o \
	  symmetry_group.o \
	  symmetry_group_closed.o \
	  symmetry_group_cusped.o \
	  symmetry_group_info.o \
	  tables.o \
	  terse_triangulation.o \
	  tersest_triangulation.o \
	  tet_shapes.o \
	  tidy_peripheral_curves.o \
	  transcendentals.o \
	  triangulations.o \
	  two_bridge.o \
          unix_UI.o \
	  unix_file_io.o \
          unix_cusped_census.o \
	  update_shapes.o \
	  volume.o

SRCS = ${OBJS:%.o=%.c}

INSTALLDIR = ../unix_kit

lib: libsnappea.a

objs: ${OBJS}

test: volume.o

libsnappea.a: ${OBJS}
	ar r libsnappea.a ${OBJS}
	ranlib libsnappea.a

.c.o:
	${CC} -c ${CFLAGS} $*.c

clean:
	rm -f *.o *~ core

distclean:
	rm -f *.o *~ libsnappea.a core

depend:
	@echo making dependency file Makefile.dependencies ...
	${CPP} ${CFLAGS} ${DEPFLAG} ${SRCS} > Makefile.dependencies
