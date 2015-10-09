/*
 *  ken2snap.c
 *
 *  Reads Millett code and computes hyperbolic invariants.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "SnapPea.h"

#define FALSE   0
#define TRUE    1


static char             describe_symmetry_action(IsometryList *aSymmetryList);
int                     compute_assorted_invariants(int option);
int                     compute_horoballs();
Triangulation *         millett_to_triangulation(char **argv);

FILE *fp1, *fp2, *gp1, *gp2;


int main(int argc, char **argv)
{
    Triangulation *theTriangulation;
    
    char *path, *file_name;
    int word_length, i, j;
    
    path = malloc(100*sizeof(char));
    file_name = malloc(100*sizeof(char));
    
    path = argv[2];
    word_length=0; while (path[word_length] != 0) ++word_length;
    i=word_length;
    while (i >= 0 && path[i] != '/') --i;
    for (j=i+1; j<=word_length; ++j) file_name[j-i-1] = path[j];
    
    fp1 = fopen(argv[1], "r");
   
    theTriangulation = millett_to_triangulation(argv);
    
    if (get_complete_solution_type(theTriangulation) >=3)
	{ 
	  fprintf(gp2, "Link is apparently non-hyperbolic\n");
	  free_triangulation(theTriangulation);
          return;
	}	

    if (theTriangulation != NULL)
    {
        
        {
            CuspNeighborhoods *theCuspNbhds;
            printf( "hello\n" );
            //theCuspNbhds = initialize_cusp_neighborhoods(theTriangulation);
            printf( "hello\n" );
        
        }
        
        set_triangulation_name(theTriangulation, file_name);
        save_triangulation(theTriangulation, argv[2]);

        free_triangulation(theTriangulation);
    }
    else
        fprintf(gp1, " ???\n");

    verify_my_malloc_usage();

    
    return 0;
}


Triangulation * millett_to_triangulation(char **argv)
{
    int             theNumCrossings, theNumComponents,
                    theIndex,
                    *crossingSign,
                    i, changed, reduced;
    char            ch;
    int             (*millettNeighbor)[4], (*millettNeighborView)[4], (*millettComponent)[2];
    KLPProjection   *theProjection;
    int             theNeighbor[2][2], theNeighborStrand[2][2];
    Triangulation   *theTriangulation;

    /*
     *  The first task is to adjust the Millett format to one that's
     *  easier for the computer to read.
     *
     */
    
    gp2 = fopen(argv[3], "w");

    while ((ch=fgetc(fp1)) != EOF)
    {
        if (ch == ':')
        {
            /* do nothing */
        }
        else if (ch == '.')
        {
            fprintf(gp2, " ");
        }
        else if (ch == '+')
        {
            fprintf(gp2, "  1  ");
        }
        else if (ch == '-')
        {
            fprintf(gp2, "  0  ");
        }
        else if (ch == 'a')
        {
            fprintf(gp2, "  1  ");
        }
        else if (ch == 'b')
        {
            fprintf(gp2, "  2  ");
        }
        else if (ch == 'c')
        {
            fprintf(gp2, "  3  ");
        }
        else if (ch == 'd')
        {
            fprintf(gp2, "  4  ");
        }
        else fputc(ch, gp2);
    }
                
    fclose(gp2);
    fp2 = fopen(argv[3], "r");

    while (fscanf(fp2, "%d%d", &theNumCrossings, &theIndex) == 2)
    {
        int i, j;
       
        /*
         *  Read the numeric Millett code
         *
         */
        
        millettNeighbor = malloc(theNumCrossings*4*sizeof(int));
        millettNeighborView = malloc(theNumCrossings*4*sizeof(int));
        crossingSign = malloc(theNumCrossings*sizeof(int));
        millettComponent = malloc(theNumCrossings*2*sizeof(int));
        
        for (i=0; i<theNumCrossings; ++i)
        {
            fscanf(fp2, "%d", &j);  /* discard */
            
            fscanf(fp2, "%d", crossingSign + i);
            
            for (j=0; j<4; ++j)
            {
                fscanf(fp2, "%d", millettNeighbor[i] + j);
                fscanf(fp2, "%d", millettNeighborView[i] + j);
                --millettNeighbor[i][j];        /* adjust to 0-based indexing */
                --millettNeighborView[i][j];
            }
        }       

        /*
         *  Label components:
         *  millettComponent[i][0] is component of overstrand at crossing i
         *  millettComponent[i][1] is component of understrand at crossing i
         *
         *  Algorithm: begin with labels all distinct, then reduce
         *
         */
        
        for (i=0; i<theNumCrossings; ++i) for (j=0; j<2; ++j)
            millettComponent[i][j] = 2*i + j;
        
        reduced = 0;
        
        while (reduced == 0)
        {
            changed = 0;
            
            for (i=0; i<theNumCrossings; ++i) for (j=0; j<4; ++j)
            {
                int u, v;
                
                u = millettNeighbor[i][j];
                v = millettNeighborView[i][j] % 2;
                if (millettComponent[i][j%2] != millettComponent[u][v])
                {
                    int comp0, comp1, r, s, temp;
                    
                    changed = 1;
                    
                    comp0 = millettComponent[i][j%2];
                    comp1 = millettComponent[u][v];
                    if (comp0 > comp1) {temp = comp0; comp0 = comp1; comp1 = temp;}
        
                    for (r=0; r<theNumCrossings; ++r) for (s=0; s<2; ++s)
                    {
                        if (millettComponent[r][s] == comp1) millettComponent[r][s] = comp0;
                        if (millettComponent[r][s] > comp1) --millettComponent[r][s];
                    }
                }
            }

            if (changed == 0) reduced = 1;
        }
        
        theNumComponents = 0;
        
        for (i=0; i<theNumCrossings; ++i) for (j=0; j<2; ++j)
            if (millettComponent[i][j] > theNumComponents)
            theNumComponents = millettComponent[i][j];
        
        ++theNumComponents;
        
        /*printf("number of components:  %2d\n", theNumComponents);*/
        
                
        /*
         *  Convert to KLPProjection format
         *
         */
        
        theProjection = (KLPProjection *) malloc(sizeof(KLPProjection));
        theProjection->num_crossings    = theNumCrossings;
        theProjection->num_free_loops   = 0;
        theProjection->num_components   = theNumComponents;
        theProjection->crossings        = (KLPCrossing *) malloc(theNumCrossings*sizeof(KLPCrossing));

        for (i=0; i<theNumCrossings; ++i)
        {
            if (crossingSign[i] == 1)
            {
                theNeighbor[KLPStrandX][KLPBackward] = millettNeighbor[i][2];
                theNeighborStrand[KLPStrandX][KLPBackward] = (crossingSign[millettNeighbor[i][2]] + millettNeighborView[i][2])%2;
                theNeighbor[KLPStrandX][KLPForward ] = millettNeighbor[i][0];
                theNeighborStrand[KLPStrandX][KLPForward ] = (crossingSign[millettNeighbor[i][0]] + millettNeighborView[i][0])%2;
                theNeighbor[KLPStrandY][KLPBackward] = millettNeighbor[i][1];
                theNeighborStrand[KLPStrandY][KLPBackward] = (crossingSign[millettNeighbor[i][1]] + millettNeighborView[i][1])%2;
                theNeighbor[KLPStrandY][KLPForward ] = millettNeighbor[i][3];
                theNeighborStrand[KLPStrandY][KLPForward ] = (crossingSign[millettNeighbor[i][3]] + millettNeighborView[i][3])%2;
            }
            else
            {
                theNeighbor[KLPStrandX][KLPBackward] = millettNeighbor[i][3];
                theNeighborStrand[KLPStrandX][KLPBackward] = (crossingSign[millettNeighbor[i][3]] + millettNeighborView[i][3])%2;
                theNeighbor[KLPStrandX][KLPForward ] = millettNeighbor[i][1];
                theNeighborStrand[KLPStrandX][KLPForward ] = (crossingSign[millettNeighbor[i][1]] + millettNeighborView[i][1])%2;
                theNeighbor[KLPStrandY][KLPBackward] = millettNeighbor[i][2];
                theNeighborStrand[KLPStrandY][KLPBackward] = (crossingSign[millettNeighbor[i][2]] + millettNeighborView[i][2])%2;
                theNeighbor[KLPStrandY][KLPForward ] = millettNeighbor[i][0];
                theNeighborStrand[KLPStrandY][KLPForward ] = (crossingSign[millettNeighbor[i][0]] + millettNeighborView[i][0])%2;
            }
            
            theProjection->crossings[i].neighbor[KLPStrandX][KLPBackward] =
                &theProjection->crossings[theNeighbor[KLPStrandX][KLPBackward]];        
            theProjection->crossings[i].neighbor[KLPStrandX][KLPForward ] =
                &theProjection->crossings[theNeighbor[KLPStrandX][KLPForward ]];
            theProjection->crossings[i].neighbor[KLPStrandY][KLPBackward] =
                &theProjection->crossings[theNeighbor[KLPStrandY][KLPBackward]];
            theProjection->crossings[i].neighbor[KLPStrandY][KLPForward ] =
                &theProjection->crossings[theNeighbor[KLPStrandY][KLPForward ]];
            
            theProjection->crossings[i].strand[KLPStrandX][KLPBackward] =
                (theNeighborStrand[KLPStrandX][KLPBackward] == 1) ? KLPStrandX : KLPStrandY;
            theProjection->crossings[i].strand[KLPStrandX][KLPForward ] =
                (theNeighborStrand[KLPStrandX][KLPForward ] == 1) ? KLPStrandX : KLPStrandY;
            theProjection->crossings[i].strand[KLPStrandY][KLPBackward] =
                (theNeighborStrand[KLPStrandY][KLPBackward] == 1) ? KLPStrandX : KLPStrandY;
            theProjection->crossings[i].strand[KLPStrandY][KLPForward ] =
                (theNeighborStrand[KLPStrandY][KLPForward ] == 1) ? KLPStrandX : KLPStrandY;
            
            theProjection->crossings[i].handedness = (crossingSign[i] == 1) ? KLPHalfTwistCL : KLPHalfTwistCCL;
            
            if (crossingSign[i] == 1)
            {
                theProjection->crossings[i].component[KLPStrandX] = millettComponent[i][0];
                theProjection->crossings[i].component[KLPStrandY] = millettComponent[i][1];
            }
            else
            {
                theProjection->crossings[i].component[KLPStrandX] = millettComponent[i][1];
                theProjection->crossings[i].component[KLPStrandY] = millettComponent[i][0];
            }
        }
     
        theTriangulation = triangulate_link_complement(theProjection);

        free(theProjection->crossings);
        free(theProjection);
	free(millettNeighbor);
        free(millettNeighborView);
        free(crossingSign);
        free(millettComponent);
    }
    
    return theTriangulation;
}


