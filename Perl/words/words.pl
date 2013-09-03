#!/usr/bin/perl

use Braid;

$braid = undef;

while (my $line = <STDIN>)
{
  if ($line =~ /(.*?)\s+(.*?)\s*$/)
  {
    my ($k,$b) = ($1,$2);
    $b =~ s/^\s*{//;
    $b =~ s/}\s*$//;
    $braid = new Braid(0,split(/,/,$b));
    print "$k : " . $braid->toString() . " : & "
      . $braid->width() . " & " . $braid->length() . "\n";
  }
}
