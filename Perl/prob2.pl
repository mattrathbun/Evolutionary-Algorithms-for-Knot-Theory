#!/usr/bin/perl

use Population;

@braids = ( );
$maxcount = 50;
$|=1;

%fitness = ( );

sub loadBraids(@)
{
  my @files = @_;
  my $maxlen = 0;
  foreach my $file (@files)
  {
    open(BRAIDS,"<$file") or warn("Unable to read $file: $!\n");
    foreach (<BRAIDS>)
    {
      if (/^\s*([\d_an]+)\s+\{([\d-,]+)\}/)
      {
	my ($knot,@crossings) = ($1,split(/,/,$2));
	my $b = new Braid(0,@crossings);
	$maxlen = ($b->length() > $maxlen ? $b->length() : $maxlen);
	push(@braids, $b);
      }
    }
    close(BRAIDS);
  }
  return $maxlen;
}

sub fitness($)
{
  my ($ol) = @_;
  my $reduced = 0;
  my $failed = 0;
  my $total = 0;
  my $flips = 0;
  my $min = $maxcount;
  my $max = 0;
  my $str = $ol->toString();
  if (defined $fitness{$str})
  {
    ($failed,$reduced,$total,$min,$max,$flips) = @{$fitness{$ol->toString()}};
  }
  else
  {
    foreach my $braid (@braids)
    {
      my $ns;
      ($ns,$flips) = numSteps($ol,$braid->copy());
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
    }
    # print "  failed = " . $failed . "\n";
    $fitness{$str} = [ $failed, $reduced, $total, $min, $max, $flips ];
  }
  my $fv = 1 + ($reduced ** 2) / ($max + $ol->length());
  # my $fv = 1 + 1000 * $reduced ** 2;
  # my $fv = 1 + (scalar(@braids) - $failed) ** 2 + ($maxcount - $max);
  return (wantarray ?
    ($fv,$failed,$reduced,$total,(scalar(@braids)-$failed),$min,$max,$flips) : $fv);
}

sub numSteps($$)
{
  my ($ol,$braid) = @_;
  # print $ol->toString() . "\n";
  # print "  " . $braid->toString() . "\n";
  my $count = 0;
  my $flips = 0;
  while ($braid->length() > 0 && $count < $maxcount)
  {
    my $fc = 0;
    $count++;
    ($braid,$fc) = $ol->apply($braid);
    # print "  " . $braid->toString() . "\n";
    $flips += $fc;
  }
  return ($count,$flips);
}

$maxlen = loadBraids(@ARGV);
print "maxlen : $maxlen\n";

$pop = new Population(50,15,1);

$ngens = ($maxlen ** 2) * 4;

$pop = new Population(200, $maxlen * 7, 1);

for (my $i = 0; $i < $ngens; $i++)
{
  print "generation " . ($i+1) . "/$ngens\n";
  $pop->iterate(\&fitness,0.1);
}

@ol = sort { fitness($b) <=> fitness($a) } $pop->toList();
# for (my $i = 0; $i < @ol; $i++)
for (my $i = 0; $i < 5; $i++)
{
  print $ol[$i]->toString() . "\n";
  my @fit = fitness($ol[$i]);
  print "  length:     " . $ol[$i]->length() . "\n";
  print "  failed:     " . $fit[1] . "\n";
  print "  reduced:    " . $fit[2] . "\n";
  print "  min:        " . $fit[5] . "\n";
  print "  max:        " . $fit[6] . "\n";
  print "  flips:      " . $ol[$i]->flipCount() . "\n";
  print "  reductions: " . $ol[$i]->reductionCount() . "\n";
}
