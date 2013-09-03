#!/usr/bin/perl

use vars qw($width $length);

die("Usage: $0 <width> <length>\n") if (@ARGV != 2);
($width,$length) = @ARGV;

print "# width = $width, length = $length\n";
listWords($width,$length,());

sub listWords($$@)
{
  my ($width,$length,@word) = @_;
  if ($length == 0)
  {
    print join(",",@word) . "\n";
  }
  else
  {
    for (my $i = -($width-1); $i < $width; $i++)
    {
      next if ($i == 0);
      listWords($width,$length-1,(@word,$i));
    }
  }
}
