/*
 *  fixedPointInfo.c
 *
 *  Reads lines of DT code, e.g.
 *
 *       9       7      6   8  10  16  14 -18   4   2 -12
 *       9       8      6 -10 -14  12 -16  -2  18  -4  -8
 *      11     126      4  10 -18 -12   2 -16 -20  -8 -22 -14  -6
 *      11     133      4  10 -18 -20   2 -16  -6  -8 -22 -14 -12
 *
 *  (the second number in each row is just the index of the knot.)
 *
 *  Outputs symmetry groups and information on individual
 *  symmetries, in particular the nature of the symmetry's
 *  fixed point set.
 */

#include <stdio.h>
#include <stdlib.h>
#include "kernel.h"

#define FALSE   0
#define TRUE    1

extern Triangulation    *DT_alpha_to_triangulation(char *aDTString);
extern Triangulation    *DT_int_to_triangulation(int aNumCrossings, int *aDTCode);
static char             describe_symmetry_action(IsometryList *aSymmetryList);

FILE *fp, *gp;

main(int argc, char **argv)
{
    char            theAlphaDT[256];
    Triangulation   *theTriangulation;
    int             theNumCrossings,
                    theIndex,
                    i, j, *theIntDT;
    
    fp = fopen(argv[1], "r");
    gp = fopen(argv[2], "w");                
    	    
    while (fscanf(fp, "%d%d", &theNumCrossings, &theIndex) == 2)
    {
        /*
         *  Echo the input to the output.
         */
        fprintf(gp, "%2d %6d\n\n", theNumCrossings, theIndex);

        /*
         *  Read the DT code.
         */
        theIntDT = (int *) malloc(theNumCrossings * sizeof(int));
        for (i = 0; i < theNumCrossings; i++)
        {
            fscanf(fp, "%d", &theIntDT[i]);
            /*
            uncomment the following line to echo the DT code to the output
            fprintf(gp, "%3d", theIntDT[i]);
            */
        }

        /*
         *  Decode theIntDT and triangulate the knot complement.
         */
        theTriangulation = DT_int_to_triangulation(theNumCrossings, theIntDT);

        /*
         *  Free the temporary array.
         */
        free(theIntDT);
	
	if (get_complete_solution_type(theTriangulation) >=3)
	{ 
	  fprintf(gp, "Knot is apparently non-hyperbolic\n\n\n");
	  free_triangulation(theTriangulation);
	  continue;
	}	


        if (theTriangulation != NULL)
        {
	
	      
	   
          IsometryList           *isometry_list=NULL;
	  Boolean                are_isometric, is_free, fullyReduced;
	  int                    i, j, k, currentTetrahedron, numTetrahedra, currentFace, imageFace,
	                         imageTet, imageVert[4], ci, numIsometries, cusp_map[2][2],
				 edgeClassIndex, (*edgeClass)[4][4], *fixedEdgeClass, 
				 vertexClassIndex, (*vertexClass)[4], *fixedVertexClass,
				 numEdges, numVertices, fixCode, groupType,
				 numFixedTetrahedra, numFixedFaces, numFixedEdges, numFixedVertices;    
	  TriangulationData      *theData;
	  Triangulation          *theCanonicalTriangulation;
          SymmetryGroup   *theManifoldSymmetryGroup=NULL, *theLinkSymmetryGroup=NULL;
          Triangulation   *unused1=NULL;
          Boolean         unused2;
	  

	  compute_symmetry_group( theTriangulation,
              &theCanonicalTriangulation,
              &theManifoldSymmetryGroup,
              &theLinkSymmetryGroup,
              &unused1,
              &unused2);

	  isometry_list = get_symmetry_list(theManifoldSymmetryGroup);
          
	  numTetrahedra = get_num_tetrahedra(theCanonicalTriangulation);

          edgeClass = malloc(numTetrahedra * 16 * 6 * sizeof(int));
	  fixedEdgeClass = malloc(numTetrahedra * 6 * sizeof(int));
	  vertexClass = malloc(numTetrahedra * 4 * 4 * sizeof(int));
	  fixedVertexClass = malloc(numTetrahedra * 4 * sizeof(int));

	  
	  triangulation_to_data(theCanonicalTriangulation, &theData);    

         /*
	  *   Group edges into gluing equivalence classes.  Use absorption algorithm (admittedly
	  *   non-geometric, but the computer quite likes it.)
	  */
	  
	  
/* bad algorithm for the given situation? Keep it for the moment. */  	  
          
	  edgeClassIndex=-1;
          for (i=0; i<=numTetrahedra-1; ++i) for (j=0; j<=2; ++j) for (k=1; k<=3; ++k) if (j < k)
            edgeClass[i][j][k] = ++edgeClassIndex;  /* This is just the initial indexing */
        
          do {
            fullyReduced=TRUE;       /*
	                              * Initially each edge is in its own equivalence class;
				      * the list of equivalence classes is steadily reduced
				      * until it is "fullyReduce"'d.
				      */
            for (i=0; i<=numTetrahedra-1; ++i) for (j=0; j<=2; ++j) for (k=1; k<=3; ++k) if (j < k)
            {
              int face[2], u;        /* 
	                              * face[0], face[1] are the faces of tetrahedron i which are
				      * incident to the edge with vertices j, k ; u is used as a
				      * placeholder for the face index.
				      */
              
              if (j > 0) face[0]=0;
              else if (k > 1) face[0]=1;
              else face[0]=2;
              face[1] = 6 - (j+k+face[0]);
              
              for (u=0; u<=1; ++u)   /* u is current face (two to process for given edge) */
              {
                int cl1, cl2, i1, j1, k1, tet, v1, v2;
                
                cl1 = edgeClass[i][j][k];
                tet = (theData -> tetrahedron_data+i) -> neighbor_index[face[u]];
                v1 = (theData -> tetrahedron_data+i) -> gluing[face[u]][j];
                v2 = (theData -> tetrahedron_data+i) -> gluing[face[u]][k];
		
                if (v1 > v2)                       /* switch v1, v2 if in the wrong order */
                { int t; t=v1; v1=v2; v2=t; }
		
                if (edgeClass[tet][v1][v2] > cl1)  /* we've found two equivalent edges with different indices */
                {
          	  fullyReduced=FALSE;              /* found guilty */
          	  cl2 = edgeClass[tet][v1][v2];
          	  for (i1=0; i1<=numTetrahedra-1; ++i1) for (j1=0; j1<=2; ++j1) for (k1=1; k1<=3; ++k1) if 
          	    (j1 < k1  &&  edgeClass[i1][j1][k1] == cl2)  /* adjust equivalence class indexing as necessary */
          	    edgeClass[i1][j1][k1] = cl1;
          	  for (i1=0; i1<=numTetrahedra-1; ++i1) for (j1=0; j1<=2; ++j1) for (k1=1; k1<=3; ++k1) if 
          	    (j1 < k1  &&  edgeClass[i1][j1][k1] > cl2)
          	    --(edgeClass[i1][j1][k1]);
                }
	      }
  	    }
	  

          } while (!fullyReduced);
	  
	  numEdges = 0;
	  
	  for (i=0; i<=numTetrahedra-1; ++i) for (j=0; j<=2; ++j) for (k=1; k<=3; ++k) if (j < k)
	  {
	    edgeClass[i][k][j] = edgeClass[i][j][k];
	    if (edgeClass[i][j][k] > numEdges) numEdges = edgeClass[i][j][k];
	  }
	  
	  ++numEdges;
	  
  
	  /*
	   *   Group vertices into equivalence classes.
	   */
	  
	  vertexClassIndex=-1;
	  for (i=0; i<=numTetrahedra-1; ++i) for (j=0; j<=3; ++j)
	    vertexClass[i][j] = ++vertexClassIndex;
	  
	  do {
	    fullyReduced=TRUE;
	  
            for (i=0; i<=numTetrahedra-1; ++i) for (j=0; j<=3; ++j) for (k=0; k<=3; ++k) if (k != j)
            {
  	      int cl1, cl2, i1, j1, k1, tet, v1, v2;
  	    
  	      cl1 = vertexClass[i][j];
              tet = (theData -> tetrahedron_data+i) -> neighbor_index[k];
              v1 = (theData -> tetrahedron_data+i) -> gluing[k][j];
  	    
  	      if (vertexClass[tet][v1] > cl1)
  	      {
  	        fullyReduced=FALSE;
  	        cl2 = vertexClass[tet][v1];
  	        for (i1=0; i1<=numTetrahedra-1; ++i1) for (j1=0; j1<=3; ++j1) if
  	          (vertexClass[i1][j1] == cl2)
  		  vertexClass[i1][j1] = cl1;
                for (i1=0; i1<=numTetrahedra-1; ++i1) for (j1=0; j1<=3; ++j1) if
  	          (vertexClass[i1][j1] > cl2)
  		  --(vertexClass[i1][j1]);
	      }
  	    }
  	  } while (!fullyReduced);
	  
	  numVertices = 0;
	  for (i=0; i<=numTetrahedra-1; ++i) for (j=0; j<=2; ++j)
	    if (vertexClass[i][j] > numVertices) numVertices = vertexClass[i][j];
    
	  numIsometries = isometry_list_size(isometry_list);
	     
	  fprintf(gp, "Isometry   M  L   Fixed point set\n\n");
	  
	  /*
	   *  Go through each symmetry, checking to see if any simplex
	   *  is mapped onto itself.
	   */
	   	  
	  groupType = 1;  /* Assume symmetry group is Zn until proved otherwise (maybe perverse) */
	   
	  for (ci=0; ci<=numIsometries-1; ++ci)
	  {
	    int v1, v2;
            
            Isometry *theIsometry = isometry_list->isometry[ci];
	    
	    numFixedTetrahedra = numFixedFaces = numFixedEdges = numFixedVertices = 0;
	    
	    for (i=0; i<=3*numTetrahedra; ++i)   
	      fixedEdgeClass[i] = fixedVertexClass[i] = 0;
	    
	    for (currentTetrahedron=0; currentTetrahedron<=numTetrahedra-1; ++currentTetrahedron)
	    {	      
	      imageTet = theIsometry->tet_image[currentTetrahedron];
              
              for ( i=0; i<4; ++i ) imageVert[i] = EVALUATE( theIsometry->tet_map[currentTetrahedron],i );          
              
              if (imageTet == currentTetrahedron)     /* This tetrahedron is mapped to itself */
	      {
	        ++numFixedTetrahedra;
              }
	      
	      for (currentFace=0; currentFace<=3; ++currentFace)
	      {
	        imageFace=imageVert[currentFace];
		
		if (((theData -> tetrahedron_data+currentTetrahedron) -> neighbor_index[currentFace] == imageTet
		  &&  (theData -> tetrahedron_data+currentTetrahedron) -> gluing[currentFace][currentFace] == imageFace)
		  ||  (currentTetrahedron == imageTet && currentFace == imageFace))
		{
		  ++numFixedFaces;
		}
	      }
	      
	      for (v1=0; v1<=2; ++v1) for(v2=1; v2<=3; ++v2) if
	        (v1 < v2  &&  edgeClass[currentTetrahedron][v1][v2] == edgeClass[imageTet][imageVert[v1]][imageVert[v2]])
	      {
	        fixedEdgeClass[edgeClass[currentTetrahedron][v1][v2]] = 1;
	      }
	      
	      for (v1=0; v1<=3; ++v1) if
	        (vertexClass[currentTetrahedron][v1] == vertexClass[imageTet][imageVert[v1]])
	      {
	        fixedVertexClass[vertexClass[currentTetrahedron][v1]] = 1;
	      }
	    }
	    
	    numFixedFaces /= 2;     /* faces come in glued pairs */
	    
	    for (i=0; i<= numEdges; ++i) if (fixedEdgeClass[i] == 1) ++numFixedEdges;
	    for (i=0; i<= numVertices; ++i) if (fixedVertexClass[i] == 1) ++numFixedVertices;
	    
	    --numFixedVertices;   /* discount the ideal vertex, as it is not a "real" vertex */
	    
	    fprintf(gp, "  %3d      ", ci + 1);
	    
	    isometry_list_cusp_action(isometry_list, ci, 0, &i, cusp_map);
	    
	    if (cusp_map[0][0] == 1) fprintf(gp, "+  "); else fprintf(gp, "-  ");
	    if (cusp_map[1][1] == 1) fprintf(gp, "+   "); else {groupType = 2; fprintf(gp, "-   ");}	/* dihedral */    
	    
	    fixCode = 0;
	    if (numFixedVertices >= 1)	 fixCode += 1;
	    if (numFixedEdges >= 1)	 fixCode += 2;
	    if (numFixedFaces >= 1)	 fixCode += 4;
	    if (numFixedTetrahedra >= 1) fixCode += 8;
	    
	    if (cusp_map[0][0] * cusp_map[1][1] == -1)
	                                                    /*
	     						     *  Symmetry reverses orientation of S^3;
	                                                     *  fixed point set is empty, S^0 or S^2.
							     */
	    {
	      if (cusp_map[1][1] == -1)
	                                                    /*
							     *  The knot is reversed, so it contains
							     *  exactly two fixed points.
							     */
	      {
	        if (fixCode == 0) fprintf(gp, "two points on knot\n");
		else fprintf(gp, "2-sphere meeting knot in two points\n");  /* impossible! */
	      }
	      
	      else
	      {
							    /*
							     *  The orientation of the knot is preserved,
							     *  so it contains no fixed point.  The fixed point
							     *  set can't be S^2, as the knot is in one
							     *  complementary component of S^2 and the
							     *  symmetry would therefore have to preserve these
							     *  complementary components.
							     */
							     
	      	if (fixCode == 0) fprintf(gp, "empty\n");
	        else fprintf(gp, "two points in complement of knot\n");
		
	      }
	    }
	    
	    if (cusp_map[0][0] * cusp_map[1][1] == 1)
	    {
							    /*
							     *  Symmetry preserves orientation of S^3;
							     *  fixed point set is empty, S^1 or S^3.
							     */
							     
	      if (cusp_map[1][1] == -1)
	      {
	        fprintf(gp, "circle meeting knot in two points\n");
	      }
	      
	      else
	      {
	        if (fixCode == 0) fprintf(gp, "empty\n");
		else if (numFixedTetrahedra == numTetrahedra && numFixedFaces == 2*numTetrahedra
		           && numFixedEdges == numEdges)
		  fprintf(gp, "S^3 (identity)\n");
		else fprintf(gp, "circle in complement of knot\n");
              }
	    }    
	  }
	  
	  if (groupType == 1) fprintf(gp, "Symmetry group: Z%1d\n\n\n", numIsometries);
	  else fprintf(gp, "Symmetry group: D%1d\n\n\n", numIsometries/2);
	  
	  free (edgeClass);
	  free (fixedEdgeClass);
	  free (vertexClass);
	  free (fixedVertexClass);
	     	   
	  free_isometry_list(isometry_list);
	   
	   
	  free_triangulation_data(theData);
	  free_triangulation(theCanonicalTriangulation);
     }
   }
   
   return 0;
}
