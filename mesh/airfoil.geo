// Comands
Include 'naca0012.geo';

// Define airfoil surface
Spline(5) = {0:32};
Spline(6) = {32:47};
Spline(7) = {47:78,0};

// Define Domain
Point(80) = {-0.1, -0.2, 0, 1.0};
Point(81) = {-0.1, 0.2, 0, 1.0};
Point(84) = {1.5, -0.2, 0, 1.0};
Point(85) = {1.5, 0.2, 0, 1.0};
Point(86) = {1.0, -0.2, 0, 1.0};
Point(87) = {1.0, 0.2, 0, 1.0};
Point(88) = {1.5, 0.0, 0, 1.0};

Line(9)  = {81, 80};
Line(10) = {80, 86}; 
Line(11) = {86, 84}; 
Line(13) = {85, 87}; 
Line(14) = {87, 81}; 
Line(15) = {87, 0}; 
Line(16) = {0, 86}; 
Line(17) = {81, 32}; 
Line(18) = {80, 47};
Line(19) = {84, 88};
Line(20) = {88, 85};
Line(21) = {88, 0};

//Front
Transfinite Curve {9, 6} = 10 Using Progression 1;
//Upper and lower surface
Transfinite Curve {5, 14, 7,  10} = 20 Using Progression 1;
//Perpendicualr direction
Transfinite Curve {17, 15, 18, 16, 20, 19} = 10 Using Progression 1;
//Wake
Transfinite Curve {13, 21, 11} = 10 Using Progression 1;

// Front Domain
Curve Loop(1) = {17, 6, -18, -9};
Plane Surface(1) = {1};
Transfinite Surface {1};

//Lower Surface Domain
Curve Loop(2) = {18, 7, 16, -10};
Plane Surface(2) = {2};
Transfinite Surface {2};

//Lower Wake Domain
Curve Loop(3) = {16, 11, 19, 21};
Plane Surface(3) = {3};
Transfinite Surface {3};

//Upper Wake Domain
Curve Loop(4) = {21, -15, -13, -20};
Plane Surface(4) = {4};
Transfinite Surface {4};

//Upper Surface Domain
Curve Loop(5) = {15, 5, -17, -14};
Plane Surface(5) = {5};
Transfinite Surface {5};

// Defines physical groups
Physical Curve("INLET", 22) = {9};
Physical Curve("UPPER_WALL", 23) = {14, 13};
Physical Curve("LOWER_WALL", 24) = {10, 11};
Physical Curve("OUTLET", 25) = {20, 19};
Physical Curve("AIRFOIL", 26) = {5, 6, 7};
Physical Surface("FLUID") = {1, 2, 3, 4, 5};