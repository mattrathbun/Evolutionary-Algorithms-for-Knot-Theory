/*
 *  knotscape_canonical.c
 *
 *  Reads a DT sequence and displays canonical cell decomposition.
 *
 *  
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "SnapPea.h"

#define FALSE   0
#define TRUE    1

extern Triangulation    *DT_int_to_triangulation(int aNumCrossings, int *aDTCode);
int                     compute_horoballs();


FILE *fp, *gp1, *gp2;

int main(int argc, char **argv)
{     
   fp = fopen(argv[1], "r");
   gp1 = fopen(argv[2], "w");
   gp2 = fopen(argv[3], "w");
   
   /*
    *  Read cut-off height for horoballs
    */
        
   compute_horoballs();
     
   return 0;
}
    

int compute_horoballs()
{
    Triangulation   *theTriangulation;
    int             theNumCrossings,
                    theIndex, 
                    *theIntDT,
                    i;


    while (fscanf(fp, "%3d%10d", &theNumCrossings, &theIndex) == 2)
    {
 
        /*
         *  Read the DT code.
         */
        theIntDT = (int *) malloc(theNumCrossings * sizeof(int));
        for (i = 0; i < theNumCrossings; i++)
        {
            fscanf(fp, "%3d", &theIntDT[i]);
            
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
	  free_triangulation(theTriangulation);
	  fprintf(gp1, "non-hyperbolic\n");
	  exit(0);
	}
	
	fprintf(gp1, "%3d %8d\n", theNumCrossings, theIndex);

        if (theTriangulation != NULL)
        {
	   CuspNeighborhoods *theCuspNbhds;
	   CuspNbhdHoroballList *theCuspNbhdHoroballList;
           CuspNbhdSegmentList *theCuspNbhdTriangSegmentList;
	   int numHoroballs, numTriangSegments,
              *startindex, *middleindex, *endindex, *valency, *invisible, **adjacency,
              *numHiddenEdges, **polygon, **polygonBack, **polygonForward, *horoball_is_edge,
              h, j, k, xl1, xl2, yl1, yl2, center_index, r, numEdges, numInvisibleEdges;
	   double *center_real, *center_imag, *radius, *edgeLength, **distance_on_horosphere,
              **forwardDistance, **backwardDistance, **hiddenEdgeLength, **hiddenDiameter,
              **center_x, **center_y, *starticd, *middleicd, *endicd, *edge_class_icd,
              *t_end0_real, *t_end0_imag, *t_end1_real, *t_end1_imag, *edgeHoroballRadiusList,
	      stopping_displacement, mx, my, lx, ly, u0, v0, u1, u2, v1, v2, u3, v3, u4, v4, u5, v5,
	      w0, w1, w2, w4, w5, x0, y0, x1, y1, x2, y2, x3, y3, x4, x5, min_x, min_y, max_x, max_y,
	      p1, p2, q1, q2, p11, p12, p21, p22, q11, q12, q21, q22, det, cut_off,
	      rad, cx, cy, d1, d2, d3, d4, rad0, rad1, rad2, badness, lineWidth, tk_scale,
	      scale_x, scale_y, translate_x, translate_y, sm,
              fx0, fx1, fx2, fx3, fy0, fy1, fy2, fy3, cosine, sine, fontSize, theCuspVolume;
	   Complex theMeridian, theLongitude;
	
	   theCuspNbhds = initialize_cusp_neighborhoods(theTriangulation);
	   
	   stopping_displacement = get_cusp_neighborhood_stopping_displacement(theCuspNbhds, 0);
	   set_cusp_neighborhood_displacement(theCuspNbhds, 0, stopping_displacement);
	   
           get_cusp_neighborhood_translations(theCuspNbhds, 0, &theMeridian, &theLongitude);
           theCuspVolume = get_cusp_neighborhood_cusp_volume(theCuspNbhds, 0);
           
           theCuspNbhdTriangSegmentList = get_cusp_neighborhood_triangulation(theCuspNbhds, 0);         
           numTriangSegments = theCuspNbhdTriangSegmentList -> num_segments;
           
           t_end0_real            = malloc(numTriangSegments * sizeof(double));
           t_end0_imag            = malloc(numTriangSegments * sizeof(double));
           t_end1_real            = malloc(numTriangSegments * sizeof(double));
           t_end1_imag            = malloc(numTriangSegments * sizeof(double));
           edgeLength             = malloc(numTriangSegments * sizeof(double));
           edgeHoroballRadiusList = malloc(numTriangSegments * sizeof(double));
           startindex             = malloc(numTriangSegments * sizeof(int));
           middleindex            = malloc(numTriangSegments * sizeof(int));
           endindex               = malloc(numTriangSegments * sizeof(int));
           starticd               = malloc(numTriangSegments * sizeof(double));
           middleicd              = malloc(numTriangSegments * sizeof(double));
           endicd                 = malloc(numTriangSegments * sizeof(double));
           edge_class_icd         = malloc(numTriangSegments * sizeof(double));
           valency                = malloc(numTriangSegments * sizeof(int));
           invisible              = malloc(numTriangSegments * sizeof(int));
           numHiddenEdges         = malloc(numTriangSegments * sizeof(int));
           distance_on_horosphere = malloc(numTriangSegments * sizeof(double *));
           adjacency              = malloc(numTriangSegments * sizeof(int *));
           polygon                = malloc(numTriangSegments * sizeof(int *));
           polygonBack            = malloc(numTriangSegments * sizeof(int *));
           polygonForward         = malloc(numTriangSegments * sizeof(int *));
           forwardDistance        = malloc(numTriangSegments * sizeof(double *));
           backwardDistance       = malloc(numTriangSegments * sizeof(double *));
           hiddenEdgeLength       = malloc(numTriangSegments * sizeof(double *));
           hiddenDiameter         = malloc(numTriangSegments * sizeof(double *));
           center_x               = malloc(numTriangSegments * sizeof(double *));
           center_y               = malloc(numTriangSegments * sizeof(double *));
           for (i=0; i<numTriangSegments; ++i) distance_on_horosphere[i] = malloc(numTriangSegments * sizeof(double));
           for (i=0; i<numTriangSegments; ++i) adjacency[i] = malloc(numTriangSegments * sizeof(int));
           for (i=0; i<numTriangSegments; ++i) polygon[i] = malloc(numTriangSegments * sizeof(int));
           for (i=0; i<numTriangSegments; ++i) polygonBack[i] = malloc(numTriangSegments * sizeof(int));
           for (i=0; i<numTriangSegments; ++i) polygonForward[i] = malloc(numTriangSegments * sizeof(int));
           for (i=0; i<numTriangSegments; ++i) forwardDistance[i] = malloc(numTriangSegments * sizeof(double));
           for (i=0; i<numTriangSegments; ++i) backwardDistance[i] = malloc(numTriangSegments * sizeof(double));
           for (i=0; i<numTriangSegments; ++i) hiddenEdgeLength[i] = malloc(numTriangSegments * sizeof(double));
           for (i=0; i<numTriangSegments; ++i) hiddenDiameter[i] = malloc(numTriangSegments * sizeof(double));
           for (i=0; i<numTriangSegments; ++i) center_x[i] = malloc(numTriangSegments * sizeof(double));
           for (i=0; i<numTriangSegments; ++i) center_y[i] = malloc(numTriangSegments * sizeof(double));
           
           
           for (i=0; i<numTriangSegments; ++i)
           {
              t_end0_real[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> endpoint[0].real;
              t_end0_imag[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> endpoint[0].imag;
              t_end1_real[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> endpoint[1].real;
              t_end1_imag[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> endpoint[1].imag;
              
              startindex[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> start_index;
              middleindex[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> middle_index;
              endindex[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> end_index;
              
              starticd[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> start_intercusp_distance;
              middleicd[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> middle_intercusp_distance;
              endicd[i] = ((theCuspNbhdTriangSegmentList -> segment) + i) -> end_intercusp_distance;
              
              edge_class_icd[middleindex[i]] = middleicd[i];
              
              edgeLength[i] = sqrt((t_end0_real[i] - t_end1_real[i])*(t_end0_real[i] - t_end1_real[i])
                 + (t_end0_imag[i] - t_end1_imag[i])*(t_end0_imag[i] - t_end1_imag[i]));
           }

           numEdges = 0;
           for (i=0; i<numTriangSegments; ++i) if (middleindex[i] > numEdges) numEdges = middleindex[i];
           ++numEdges;    /* because of 0-based indexing */
           
           /*
            *  Calculate cut-off diameter needed for display of edges of canonical decomposition
            */  

           cut_off = 1;
           for (i=0; i<numTriangSegments; ++i) if (exp(-middleicd[i]) < cut_off)
              cut_off = exp(-middleicd[i]);
           cut_off -= 1E-6;
           
           
           /*
            *  Now compute centers and radii of horoballs
            */
            
           theCuspNbhdHoroballList = get_cusp_neighborhood_horoballs(theCuspNbhds, 0, 1, cut_off);
	   numHoroballs = theCuspNbhdHoroballList -> num_horoballs;
           
           badness = sqrt(numTriangSegments*theLongitude.real*theLongitude.real/theCuspVolume);

           if (badness <= 100) fontSize = 300/badness;
           else fontSize = 1.5;
                     
           lineWidth = fontSize/30;
           
           center_real = malloc(numHoroballs * sizeof(double));
           center_imag = malloc(numHoroballs * sizeof(double));
           radius = malloc(numHoroballs * sizeof(double));
           horoball_is_edge= malloc(numHoroballs * sizeof(int));
	   for (i=0; i<numHoroballs; ++i)
	   {
	      radius[i] = ((theCuspNbhdHoroballList -> horoball) + i) -> radius;
	      center_real[i] = ((theCuspNbhdHoroballList -> horoball) + i) -> center.real;
	      center_imag[i] = ((theCuspNbhdHoroballList -> horoball) + i) -> center.imag;
	   }
           
           /*
            *  Find which horoballs have radius equal to that of an edge horoball.
            */
           
           for (i=0; i<numTriangSegments; ++i) edgeHoroballRadiusList[i] = exp(-middleicd[i])/2;
           
           for (i=0; i<numHoroballs; ++i) horoball_is_edge[i] = 0;
            
           for (i=0; i<numHoroballs; ++i)
           {
              for (j=0; j<numTriangSegments; ++j) if (fabs(radius[i] - edgeHoroballRadiusList[j]) < 1E-6)
              {
                 horoball_is_edge[i] = 1;
                 continue;
              }
	   }
           
           /*
            *  In symmetric situations, we might have faces with more than three sides.
            *  At the moment such faces are triangulated:  we need to determine the
            *  interior edges of such faces, as we don't want to display these.
            */
           
           
           for (i=0; i<numTriangSegments; ++i) valency[i] = invisible[i] = numHiddenEdges[i] = 0;
           
           for (i=0; i<numTriangSegments; ++i)
           {
              ++valency[startindex[i]];
              ++valency[endindex[i]];
           }
           
           /*
            *  An edge is invisible iff it has valency 4 .
            */
           
           numInvisibleEdges = 0;
           for (i=0; i<numEdges; ++i) if (valency[i] == 4)
           {
              ++numInvisibleEdges;
              invisible[i] = 1;
           }
           
           /*
            *  adjacency[r][s] == t  means that horizontal edges with labels r, t meet at invisible
            *  vertical edge with label s .
            */
           

           for (i=0; i<numTriangSegments; ++i) for (j=0; j<numTriangSegments; ++j) adjacency[i][j] = -1;
           
           for (i=0; i<numTriangSegments; ++i) for (j=0; j<i; ++j)
           {
              double u0x, u0y, u1x, u1y, v0x, v0y, v1x, v1y;
              
              u0x = t_end0_real[i]; u0y = t_end0_imag[i]; u1x = t_end1_real[i]; u1y = t_end1_imag[i];
              v0x = t_end0_real[j]; v0y = t_end0_imag[j]; v1x = t_end1_real[j]; v1y = t_end1_imag[j];
              
              if (invisible[startindex[i]] == 1 && invisible[startindex[j]] == 1 &&
                  whether_translate_equivalent(u0x, u0y, v0x, v0y, theMeridian, theLongitude) == 1)
              {
                 adjacency[middleindex[i]][startindex[i]] = middleindex[j];
                 adjacency[middleindex[j]][startindex[j]] = middleindex[i];
              }
              if (invisible[startindex[i]] == 1 && invisible[endindex[j]] == 1 &&
                  whether_translate_equivalent(u0x, u0y, v1x, v1y, theMeridian, theLongitude) == 1)
              {
                 adjacency[middleindex[i]][startindex[i]] = middleindex[j];
                 adjacency[middleindex[j]][endindex[j]] = middleindex[i];
              }
              if (invisible[endindex[i]] == 1 && invisible[startindex[j]] == 1 &&
                  whether_translate_equivalent(u1x, u1y, v0x, v0y, theMeridian, theLongitude) == 1)
              {
                 adjacency[middleindex[i]][endindex[i]] = middleindex[j];
                 adjacency[middleindex[j]][startindex[j]] = middleindex[i];
              }
              if (invisible[endindex[i]] == 1 && invisible[endindex[j]] == 1 &&
                  whether_translate_equivalent(u1x, u1y, v1x, v1y, theMeridian, theLongitude) == 1)
              {
                 adjacency[middleindex[i]][endindex[i]] = middleindex[j];
                 adjacency[middleindex[j]][endindex[j]] = middleindex[i];
              }
           }
           

           /*
            *  Each invisible edge spans a polygon, and thus its endpoints separate
            *  the polygon's edges into two sets.  When the invisible edge is
            *  displayed horizontally, it hides one of these two sets of edges.
            *  We find the labels of these hidden edges by repeatedly peeling away
            *  invisible edges.
            */
           
           for (i=0; i<numTriangSegments; ++i) if (invisible[middleindex[i]] == 1)
           {
              center_x[i][0] = t_end0_real[i];
              center_y[i][0] = t_end0_imag[i];
              
              hiddenDiameter[i][0] = exp(-starticd[i]);
              
              for (j=0; j<0; ++j)    /* Find diameter of first horoball */
              {
                 if (whether_translate_equivalent(center_x[i][0], center_y[i][0], center_real[j], center_imag[j], theMeridian, theLongitude) == 1)
                 {
                    hiddenDiameter[i][0] = 2*radius[j];
                    break;
                 }
              }
            
              numHiddenEdges[i] = 1;
              polygon[i][0] = middleindex[i];
              polygonBack[i][0] = startindex[i];
              polygonForward[i][0] = endindex[i];
              
              distance_on_horosphere[i][0] = sqrt(exp(-edge_class_icd[middleindex[i]]) * exp(-edge_class_icd[startindex[i]]) / exp(-edge_class_icd[endindex[i]]));
              distance_on_horosphere[i][1] = sqrt(exp(-edge_class_icd[middleindex[i]]) * exp(-edge_class_icd[endindex[i]]) / exp(-edge_class_icd[startindex[i]]));
            
              for (j=0; j<numHiddenEdges[i]; ++j) if (invisible[polygon[i][j]] == 1)
              {
                 int p1, p2, q1, q2, r1, r2;
                 
                 distance_on_horosphere[i][numHiddenEdges[i]+1] = distance_on_horosphere[i][numHiddenEdges[i]];
                 
                 for (k=numHiddenEdges[i]-1; k >= j+1; --k)             /* Shift to make room for extra edge */
                 {
                    polygon[i][k+1] = polygon[i][k];
                    polygonBack[i][k+1] = polygonBack[i][k];
                    polygonForward[i][k+1] = polygonForward[i][k];
                    distance_on_horosphere[i][k+1] = distance_on_horosphere[i][k];
                 }
                                                                        /* q1, q2 are the edges hidden immediately below current edge */
                 q1 = adjacency[polygonBack[i][j]][polygon[i][j]];      
                 q2 = adjacency[polygonForward[i][j]][polygon[i][j]];   
                 p1 = polygon[i][j];                                    
                 p2 = q1;                                               
                 r1 = q2;
                 r2 = p1;

                 polygonBack[i][j] = p1;
                 polygonBack[i][j+1] = p2;
                 polygon[i][j] = q1;
                 polygon[i][j+1] = q2;
                 polygonForward[i][j] = r1;
                 polygonForward[i][j+1] = r2;
                 
                 distance_on_horosphere[i][j]   += sqrt(exp(-edge_class_icd[q1]) * exp(-edge_class_icd[p1]) / exp(-edge_class_icd[q2]));
                 distance_on_horosphere[i][j+1]  = sqrt(exp(-edge_class_icd[q2]) * exp(-edge_class_icd[q1]) / exp(-edge_class_icd[p1]));
                 distance_on_horosphere[i][j+2] += sqrt(exp(-edge_class_icd[p1]) * exp(-edge_class_icd[q2]) / exp(-edge_class_icd[q1]));
                                             
                 ++numHiddenEdges[i];                     /* We now have one more hidden edge than previously */
                 --j;                                     /* Must redo this particular j, as new edge q1 might be invisible */
              }
            
              backwardDistance[i][0] = 0;
              
              for (j=0; j<numHiddenEdges[i]; ++j)
              {
                 forwardDistance[i][j]  = distance_on_horosphere[i][j] - backwardDistance[i][j];
                 hiddenEdgeLength[i][j] = hiddenDiameter[i][j] / forwardDistance[i][j];
                 hiddenDiameter[i][j+1] = (hiddenEdgeLength[i][j] * hiddenEdgeLength[i][j]) / (hiddenDiameter[i][j] * exp(edge_class_icd[polygon[i][j]]));
                 backwardDistance[i][j+1] = hiddenDiameter[i][j+1] / hiddenEdgeLength[i][j];
              }
            
              cosine = (t_end1_real[i] - t_end0_real[i]) / edgeLength[i];
              sine   = (t_end1_imag[i] - t_end0_imag[i]) / edgeLength[i];
              
              for (j=1; j<=numHiddenEdges[i]; ++j)
              {
                 center_x[i][j] = center_x[i][j-1] + cosine * hiddenEdgeLength[i][j-1];
                 center_y[i][j] = center_y[i][j-1] +   sine * hiddenEdgeLength[i][j-1];
              }
           }
      
	   
	   /*
	    *  Scale so that fundamental region fits nicely in canvas
	    *  of dimensions 800x600.  First locate lowest leftmost
	    *  horoball of maximal radius.
	    */
	   
	   min_x = min_y = 1000.0;    /* impossibly large */
	   
	   for (i=0; i<numHoroballs; ++i) if (radius[i] > .499999)
	   {
	      if (center_real[i] + center_imag[i] < min_x + min_y)
	      {
	        min_x = center_real[i];
		min_y = center_imag[i];
              }	      
	   }
	   
	   max_x = min_x + theMeridian.real + theLongitude.real;
	   max_y = min_y + theMeridian.imag + theLongitude.imag;
	   
	   if (theMeridian.real >= 0)
	      scale_x = 600/(max_x - min_x);
	   else
	      scale_x = 600/(max_x - min_x - 2*theMeridian.real);
	   translate_x  =  400  -  scale_x * (min_x + max_x) / 2;
	   scale_y = scale_x;
	   translate_y  =  300  -  scale_y * (min_y + max_y) / 2;
	   
	   for (i=0; i<numHoroballs; ++i)
	   {
	      center_real[i] = center_real[i] * scale_x + translate_x;
	      center_imag[i] = center_imag[i] * scale_y + translate_y;
	      radius[i] = radius[i] * scale_x;
	   }
           
           for (i=0; i<numTriangSegments; ++i)
	   {
	      t_end0_real[i] = t_end0_real[i] * scale_x + translate_x;
	      t_end0_imag[i] = t_end0_imag[i] * scale_y + translate_y;
	      t_end1_real[i] = t_end1_real[i] * scale_x + translate_x;
              t_end1_imag[i] = t_end1_imag[i] * scale_y + translate_y;
	   }
           
           for (i=0; i<numTriangSegments; ++i) if (invisible[middleindex[i]] == 1)
              for (j=0; j<=numHiddenEdges[i]; ++j)
              {
                 center_x[i][j] = center_x[i][j] * scale_x + translate_x;
                 center_y[i][j] = center_y[i][j] * scale_y + translate_y;
              }
           
	   
	   theMeridian.real *= scale_x;
	   theMeridian.imag *= scale_x;
	   theLongitude.real *= scale_x;
	   theLongitude.imag *= scale_x;
	   
	   
	   min_x = min_x * scale_x + translate_x;
	   max_x = max_x * scale_x + translate_x;
	   min_y = min_y * scale_y + translate_y;
	   max_y = max_y * scale_y + translate_y;
           
           /*
            *  Vertices of boundary of fundamental region
            */
            
           fx0 = min_x;
	   fy0 = min_y;
	   fx1 = fx0 + theMeridian.real;
	   fy1 = fy0 + theMeridian.imag;
	   fx2 = max_x;
	   fy2 = max_y;
	   fx3 = fx0 + theLongitude.real;
	   fy3 = fy0 + theLongitude.imag;
           
           tk_scale = pow((badness/9.11), 0.7);
           
           fprintf(gp1, "% 9.4f\n", tk_scale);
           
           fprintf(gp1, "% 9.4f % 9.4f\n", fx0*tk_scale, (600-fy0)*tk_scale);
	   fprintf(gp1, "% 9.4f % 9.4f\n", fx1*tk_scale, (600-fy1)*tk_scale);
	   fprintf(gp1, "% 9.4f % 9.4f\n", fx2*tk_scale, (600-fy2)*tk_scale);
	   fprintf(gp1, "% 9.4f % 9.4f\n", fx3*tk_scale, (600-fy3)*tk_scale);
           
           /*
	    *   Write Postscript file header
	    */
	    
	   fprintf(gp2, "%%!PS-Adobe-3.0 EPSF-3.0\n");
	   fprintf(gp2, "%%%%Title: Horoball Diagram of Knot %1d.%1d ;  Cut-off Diameter: %4.2f\n",
	                 theNumCrossings, theIndex, cut_off);
	   fprintf(gp2, "%%%%BoundingBox: 0 0 600 800\n");
	   fprintf(gp2, "%%%%Pages: 1\n");
	   fprintf(gp2, "%%%%DocumentData: Clean7Bit\n");
	   fprintf(gp2, "%%%%Orientation: Portrait\n");
	   fprintf(gp2, "%%%%EndComments\n");
	   fprintf(gp2, "%%%%Page: 1 1\n\n");
           
	 
           fprintf(gp2, "605 0 translate\n");
	   fprintf(gp2, "90 rotate\n\n");
	   fprintf(gp2, "50 562.5 moveto 750 562.5 lineto 750 37.5 lineto 50 37.5 lineto closepath\n");
	   fprintf(gp2, "clip newpath\n");
	   fprintf(gp2, "1 setlinewidth\n");
	   fprintf(gp2, "50 562.5 moveto 750 562.5 lineto 750 37.5 lineto 50 37.5 lineto closepath\n");
	   fprintf(gp2, "400 300 translate 7 8 div dup scale -400 -300 translate\n");
           fprintf(gp2, "stroke\n\n");
         
           fprintf(gp2, "2 setlinewidth\n");
           fprintf(gp2, "0 1 0 setrgbcolor\n");
	   fprintf(gp2, "% 9.4f % 9.4f  moveto\n", fx0, fy0);
	   fprintf(gp2, "% 9.4f % 9.4f  lineto\n", fx1, fy1);
	   fprintf(gp2, "% 9.4f % 9.4f  lineto\n", fx2, fy2);
	   fprintf(gp2, "% 9.4f % 9.4f  lineto\n", fx3, fy3);
	   fprintf(gp2, "closepath\n\n");
           fprintf(gp2, "stroke\n\n");
           fprintf(gp2, "0 0 0 setrgbcolor\n");
           fprintf(gp2, "% 4.3lf setlinewidth\n", lineWidth);
           fprintf(gp2, "/TimesBold findfont %6.3lf scalefont setfont\n", fontSize);
         
	   /*
	    *   find all translates which fit inside canvas, i.e.
	    *   whose centers satisfy  0 < x < 800 and 0 < y < 600
	    */
	   
	   mx = theMeridian.real;
	   my = theMeridian.imag;
	   lx = theLongitude.real;
	   ly = theLongitude.imag;
	   
	   /*
	    *   find coordinates of bounding box for original horoballs
	    */
	    
	   min_x = 1000.0;	   
	   for (i=0; i<=numHoroballs-1; ++i) if (center_real[i] - radius[i] < min_x)
	     min_x = center_real[i] - radius[i];
	   min_y = 1000.0;
	   for (i=0; i<=numHoroballs-1; ++i) if (center_imag[i] - radius[i] < min_y)
	     min_y = center_imag[i] - radius[i];
	   max_x = -1000.0;
	   for (i=0; i<=numHoroballs-1; ++i) if (center_real[i] + radius[i] > max_x)
	     max_x = center_real[i] + radius[i];
	   max_y = -1000.0;
	   for (i=0; i<=numHoroballs-1; ++i) if (center_imag[i] + radius[i] > max_y)
	     max_y = center_imag[i] + radius[i];
	   
	   /*
	    *   work out range of linear combinations needed to
	    *   fill canvas.  Solve system of two equations.
	    */
	   
	   det = lx*my - mx*ly;     /* determinant of system */
	   
	   p11 = (1/det)*(my*(-max_x) - mx*(-max_y));
	   q11 = (1/det)*(-ly*(-max_x) + lx*(-max_y));
	   p12 = (1/det)*(my*(800-min_x) - mx*(-max_y));
	   q12 = (1/det)*(-ly*(800-min_x) + lx*(-max_y));
	   p21 = (1/det)*(my*(800-min_x) - mx*(600-min_y));
	   q21 = (1/det)*(-ly*(800-min_x) + lx*(600-min_y));
	   p22 = (1/det)*(my*(-max_x) - mx*(600-min_y));
	   q22 = (1/det)*(-ly*(-max_x) + lx*(600-min_y));
 
	   if (p11 < p12) p1 = p11; else p1 = p12;
	   if (p21 < p1) p1 = p21;
	   if (p22 < p1) p1 = p22;
	   p1 = floor(p1);
	
	   if (p11 > p12) p2 = p11; else p2 = p12;
	   if (p21 > p2) p2 = p21;
	   if (p22 > p2) p2 = p22;
	   p2 = ceil(p2);
	   
	   if (q11 < q12) q1 = q11; else q1 = q12;
	   if (q21 < q1) q1 = q21;
	   if (q22 < q1) q1 = q22;
	   q1 = floor(q1);
	
	   if (q11 > q12) q2 = q11; else q2 = q12;
	   if (q21 > q2) q2 = q21;
	   if (q22 > q2) q2 = q22;
	   q2 = ceil(q2);
  
	   xl1 = (int) p1;
	   xl2 = (int) p2;
	   yl1 = (int) q1;
	   yl2 = (int) q2;
	   
           
	   /*
	    *   print parameters needed by tk to draw circles, and also print to PostScript file
	    */
           
           sm = scale_x * 1.5;
         
	   for (i=0; i<numHoroballs; ++i)
	      for (j=xl1; j<=xl2; ++j) for (k=yl1; k<=yl2; ++k)
	         if (center_real[i] + radius[i] + j*lx + k*mx >  -sm &&
		     center_real[i] - radius[i] + j*lx + k*mx <  800+sm &&
		     center_imag[i] + radius[i] + j*ly + k*my >  -sm &&
		     center_imag[i] - radius[i] + j*ly + k*my <  600+sm)   
		 {
		    u0 = center_real[i] + j*lx + k*mx - radius[i];
		    v0 = center_imag[i] + j*ly + k*my - radius[i];
		    u1 = center_real[i] + j*lx + k*mx + radius[i];
		    v1 = center_imag[i] + j*ly + k*my + radius[i];
                    
                    fprintf(gp1, "h % 9.4f % 9.4f % 9.4f % 9.4f\n", u0*tk_scale, (600-v0)*tk_scale, u1*tk_scale, (600-v1)*tk_scale);
                   
                    rad = radius[i];
		    cx = u0 + rad;
		    cy = v0 + rad;
		    x0 = u1;
		    y0 = cy;
                   
		    fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", x0, y0);
		    fprintf(gp2, "% 9.4f  % 9.4f  % 9.4f   0 360 arc\n", cx, cy, rad);
	         }

           fprintf(gp2, "stroke\n");
           fprintf(gp2, "0 0 1 setrgbcolor\n");
           
           for (i=0; i<numTriangSegments; ++i)
              for (j=xl1; j<=xl2; ++j) for (k=yl1; k<=yl2; ++k)
                 if (t_end0_real[i] + j*lx + k*mx > -sm &&
		     t_end0_real[i] + j*lx + k*mx < 800+sm &&
		     t_end0_imag[i] + j*ly + k*my > -sm &&
		     t_end0_imag[i] + j*ly + k*my < 600+sm)
		 {
                    u0 = t_end0_real[i] + j*lx + k*mx;
                    v0 = t_end0_imag[i] + j*ly + k*my;
                    u1 = t_end1_real[i] + j*lx + k*mx;
                    v1 = t_end1_imag[i] + j*ly + k*my;
                    
                    fprintf(gp1, "s  % 9.4f  % 9.4f  % 9.4f  % 9.4f\n", u0*tk_scale, (600-v0)*tk_scale, u1*tk_scale, (600-v1)*tk_scale);
                    
                    fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", u0, v0);
                    fprintf(gp2, "% 9.4f  % 9.4f  lineto\n", u1, v1);
	         }
                 
           fprintf(gp2, "stroke\n");
           fprintf(gp2, "0 0 0 setrgbcolor\n");
           
           for (i=0; i<numHoroballs; ++i) if (horoball_is_edge[i] == 1)
           {
	      for (j=xl1; j<=xl2; ++j) for (k=yl1; k<=yl2; ++k)
	         if (center_real[i] + radius[i] + j*lx + k*mx >  -sm &&
		     center_real[i] - radius[i] + j*lx + k*mx <  800+sm &&
		     center_imag[i] + radius[i] + j*ly + k*my >  -sm &&
		     center_imag[i] - radius[i] + j*ly + k*my <  600+sm)   
		 {
		    u0 = center_real[i] + j*lx + k*mx - 5/tk_scale;
		    v0 = center_imag[i] + j*ly + k*my - 5/tk_scale;
		    u1 = center_real[i] + j*lx + k*mx + 5/tk_scale;
		    v1 = center_imag[i] + j*ly + k*my + 5/tk_scale;
                    
                    fprintf(gp1, "b % 9.4f % 9.4f % 9.4f % 9.4f\n", u0*tk_scale, (600-v0)*tk_scale, u1*tk_scale, (600-v1)*tk_scale);
	         }
           }
                 
           for (i=0; i<numTriangSegments; ++i)
              for (j=xl1; j<=xl2; ++j) for (k=yl1; k<=yl2; ++k)
                 if (t_end0_real[i] + j*lx + k*mx > -sm &&
		     t_end0_real[i] + j*lx + k*mx < 800+sm &&
		     t_end0_imag[i] + j*ly + k*my > -sm &&
		     t_end0_imag[i] + j*ly + k*my < 600+sm)
                 {
                    int k1;
                    
                    u0 = t_end0_real[i] + j*lx + k*mx;
                    v0 = t_end0_imag[i] + j*ly + k*my;
                    u1 = t_end1_real[i] + j*lx + k*mx;
                    v1 = t_end1_imag[i] + j*ly + k*my;
                    
                    
                    if (invisible[startindex[i]] == 0)
                    {
                       fprintf(gp1, "l1  % 9.4f  % 9.4f  %3d\n", u0*tk_scale, (600-v0)*tk_scale, startindex[i]);
                       fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", u0-fontSize/3, v0-fontSize/3);
                       fprintf(gp2, "(%1d) show\n", startindex[i]);
                    }
                    else
                    {
                       fprintf(gp1, "q  % 9.4f  % 9.4f\n", u0*tk_scale, (600-v0)*tk_scale);
                       fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", u0-60/badness, v0-60/badness);
                       fprintf(gp2, "% 9.4f  % 9.4f lineto % 9.4f  % 9.4f lineto % 9.4f  % 9.4f lineto closepath fill\n",
                          u0+60/badness, v0-60/badness, u0+60/badness, v0+60/badness, u0-60/badness, v0+60/badness);
                    }
                    
                    if (invisible[endindex[i]] == 0)
                    {
                       fprintf(gp1, "l1  % 9.4f  % 9.4f  %3d\n", u1*tk_scale, (600-v1)*tk_scale, endindex[i]);
                       fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", u1-fontSize/3, v1-fontSize/3);
                       fprintf(gp2, "(%1d) show\n", endindex[i]);
                    }
                    else
                    {
                       fprintf(gp1, "q  % 9.4f  % 9.4f\n", u1*tk_scale, (600-v1)*tk_scale);
                       fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", u1-60/badness, v1-60/badness);
                       fprintf(gp2, "% 9.4f  % 9.4f lineto % 9.4f  % 9.4f lineto % 9.4f  % 9.4f lineto closepath fill\n",
                          u1+60/badness, v1-60/badness, u1+60/badness, v1+60/badness, u1-60/badness, v1+60/badness);
                    }
                    
                    if (invisible[middleindex[i]] == 1)
                    {   
                       for (k1=1; k1<numHiddenEdges[i]; ++k1)
                       {
                          u0 = center_x[i][k1]    + j*lx + k*mx;
                          v0 = center_y[i][k1]    + j*ly + k*my;
                          
                          fprintf(gp1, "q  % 9.4f  % 9.4f\n", u0*tk_scale, (600-v0)*tk_scale);
                          fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", u0-60/badness, v0-60/badness);
                          fprintf(gp2, "% 9.4f  % 9.4f lineto % 9.4f  % 9.4f lineto % 9.4f  % 9.4f lineto closepath fill\n",
                             u0+60/badness, v0-60/badness, u0+60/badness, v0+60/badness, u0-60/badness, v0+60/badness);
                       }
                    }
                 }
           
           fprintf(gp2, "stroke\n");
           fprintf(gp2, "0 0 1 setrgbcolor\n");
                
           for (i=0; i<numTriangSegments; ++i)
              for (j=xl1; j<=xl2; ++j) for (k=yl1; k<=yl2; ++k)
                 if (t_end0_real[i] + j*lx + k*mx > -sm &&
		     t_end0_real[i] + j*lx + k*mx < 800+sm &&
		     t_end0_imag[i] + j*ly + k*my > -sm &&
		     t_end0_imag[i] + j*ly + k*my < 600+sm)
                 {
                    int k1;
                    
                    u0 = t_end0_real[i] + j*lx + k*mx;
                    v0 = t_end0_imag[i] + j*ly + k*my;
                    u1 = t_end1_real[i] + j*lx + k*mx;
                    v1 = t_end1_imag[i] + j*ly + k*my;
                 
                    if (invisible[middleindex[i]] == 0)
                    {
                       fprintf(gp1, "l2  % 9.4f  % 9.4f  %3d\n", tk_scale*(u0+u1)/2, tk_scale*(600-(v0+v1)/2), middleindex[i]);
                       fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", (u0+u1)/2-fontSize/3, (v0+v1)/2-fontSize/3);
                       fprintf(gp2, "(%1d) show\n", middleindex[i]);
                    }
                    else
                    for (k1=0; k1<numHiddenEdges[i]; ++k1)
                    {
                       u0 = center_x[i][k1]    + j*lx + k*mx;
                       v0 = center_y[i][k1]    + j*ly + k*my;
                       u1 = center_x[i][k1+1]  + j*lx + k*mx;
                       v1 = center_y[i][k1+1]  + j*ly + k*my;
                       
                       fprintf(gp1, "l2  % 9.4f  % 9.4f  %3d\n", tk_scale*(u0+u1)/2, tk_scale*(600-(v0+v1)/2), polygon[i][k1]);
                       fprintf(gp2, "% 9.4f  % 9.4f  moveto\n", (u0+u1)/2-fontSize/3, (v0+v1)/2-fontSize/3);
                       fprintf(gp2, "(%1d) show\n", polygon[i][k1]);
                    }
                 }
           
           fprintf(gp2, "stroke\n");
           
	   /*
	    *   Write epilog of Postscript file
	    */
	   
	   fprintf(gp2, "stroke\n");
	   fprintf(gp2, "showpage\n");
	   fprintf(gp2, "%%%%EOF\n"); 
	   
	   free_cusp_neighborhood_horoball_list(theCuspNbhdHoroballList);
           free_cusp_neighborhood_segment_list(theCuspNbhdTriangSegmentList);
	   free_cusp_neighborhoods(theCuspNbhds);

           free_triangulation(theTriangulation);

           free(t_end0_real);
           free(t_end0_imag);
           free(t_end1_real);
           free(t_end1_imag);
           free(edgeLength);
           free(startindex);
           free(middleindex);
           free(endindex);
           free(valency);
           free(invisible);
           free(numHiddenEdges);

           for (i=0; i<numTriangSegments; ++i) free(distance_on_horosphere[i]);
           for (i=0; i<numTriangSegments; ++i) free(adjacency[i]);
           for (i=0; i<numTriangSegments; ++i) free(polygon[i]);
           for (i=0; i<numTriangSegments; ++i) free(polygonBack[i]);
           for (i=0; i<numTriangSegments; ++i) free(polygonForward[i]);
           for (i=0; i<numTriangSegments; ++i) free(forwardDistance[i]);
           for (i=0; i<numTriangSegments; ++i) free(backwardDistance[i]);
           for (i=0; i<numTriangSegments; ++i) free(hiddenEdgeLength[i]);
           for (i=0; i<numTriangSegments; ++i) free(hiddenDiameter[i]);
           
           free(distance_on_horosphere);
           free(adjacency);
           free(polygon);
           free(polygonBack);
           free(polygonForward);
           free(forwardDistance);
           free(backwardDistance);
           free(hiddenEdgeLength);
           free(hiddenDiameter);
           
           for (i=0; i<numTriangSegments; ++i) free(center_x[i]);
           for (i=0; i<numTriangSegments; ++i) free(center_y[i]);
           
           free(center_x);
           free(center_y);
        }
        else
           printf(" ???\n");

        verify_my_malloc_usage();
    }
    
    
 
    
    return 0;
    
}


whether_translate_equivalent(double u1, double v1, double u2, double v2, Complex theMeridian, Complex theLongitude)
{
   double det, x, y, lambda, kappa;

   det = theMeridian.real * theLongitude.imag  -  theMeridian.imag * theLongitude.real;
   
   x = u1 - u2;
   y = v1 - v2;
   
   lambda = (1/det) * (theLongitude.imag * x - theLongitude.real * y);
   kappa  = (1/det) * (-theMeridian.imag * x +  theMeridian.real * y);

   /*  Now test the coefficients lambda, kappa to see if they're both integers. */
   
   if ((fabs(floor(lambda) - lambda) < 1E-6 || fabs(ceil(lambda) - lambda) < 1E-6)
       &&  (fabs(floor(kappa) - kappa) < 1E-6 || fabs(ceil(kappa) - kappa) < 1E-6))
      return 1;
   
   else return 0;
}
