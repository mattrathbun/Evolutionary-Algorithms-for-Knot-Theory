#!/usr/bin/perl

use Population;

$braid = undef;
$maxcount = 50;
$|=1;

%fitness = ( );

sub parseBraid()
{
  my $argv = join(",",@ARGV);
  my @args = split(/\s*[\s,]\s*/,$argv);
  $braid = new Braid(0,@args);
}

sub fitness($)
{
  my ($ol) = @_;
  my $reduced = 0;
  my $failed = 0;
  my $total = 0;
  my $flips = 0;
  my $rl = 0;
  my $min = $maxcount;
  my $max = 0;
  my $str = $ol->toString();
  if (defined $fitness{$str})
  {
    ($failed,$reduced,$total,$min,$max,$flips,$rl) =
      @{$fitness{$ol->toString()}};
  }
  else
  {
    my $ns;
    my $nl;
    ($ns,$flips,$nl) = numSteps($ol,$braid->copy());
    if ($ns == $maxcount)
    {
      $failed++;
    }
    else
    {
      $reduced++;
    }
    $total += $ns;
    $min = ($ns < $min ? $ns : $min);
    $max = ($ns > $max  && $ns != $maxcount ? $ns : $max);
    $rl = $nl->length();
    # print "  failed = " . $failed . "\n";
    $fitness{$str} = [ $failed, $reduced, $total, $min, $max, $flips, $rl ];
  }
  # my $fv = ($reduced * 100000) /
  # (($flips ** 2) * ($ol->length()) * ($max) + 1);
  # my $fv = $reduced
  # * (100000 - 10 * $flips ** 2 )
  # * ($max > 1 ? 0.1 : 1)
  # / (10 * $ol->length() )
  # + 1
  # ;
  my $fv = 10000 * ($reduced * ($max > 1 ? 0 : 1) /
    ($rl + ($flips ** 3)+1)) + 1;
  # my $fv = 1 + $reduced ** 2 + ($maxcount - $max);
  # my $fv = 1 + (scalar(@braids) - $failed) ** 2 + ($maxcount - $max);
  return (wantarray ?
    ($fv,$failed,$reduced,$total,$min,$max,$flips) : $fv);
}

sub numSteps($$)
{
  my ($ol,$braid) = @_;
  # print $ol->toString() . "\n";
  # print "  " . $braid->toString() . "\n";
  my ($braid,$flips,$nl) = $ol->apply($braid);
  $count = ($braid->length() > 0 ? $maxcount : 1);
  return ($count,$flips,$nl);
}

parseBraid();
#$ngens = ($braid->length() ** 2) * 4;
$ngens = ($braid->length() ** 2) * 2;

$pop = new Population(500, $braid->length() * 7, 1);

for (my $i = 0; $i < $ngens; $i++)
{
  print "generation " . ($i+1) . " / $ngens\n";
  $pop->iterate(\&fitness,0.2);
}

@ol = sort { fitness($b) <=> fitness($a) } $pop->toList();
#for (my $i = 0; $i < @ol; $i++)
for (my $i = 0; $i < 3; $i++)
{
  my (undef,undef,$nl) = $ol[$i]->apply($braid);
  print $ol[$i]->toString() . "\n";
  print $nl->toString() . "\n";
  my @fit = fitness($nl);
  print "  length:     " . $nl->length() . "\n";
  print "  failed:     " . $fit[1] . "\n";
  print "  reduced:    " . $fit[2] . "\n";
  print "  min:        " . $fit[4] . "\n";
  print "  max:        " . $fit[5] . "\n";
  print "  flips:      " . $fit[6] . "\n";
  print "  reductions: " . $nl->reductionCount() . "\n";
}
