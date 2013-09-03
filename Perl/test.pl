#!/usr/bin/perl

use Braid;

$b = new Braid(2,(1,-1,1,-1,1));

print $b->toString() . "\n";
$b->reduceOneR2();
print $b->toString() . "\n";

