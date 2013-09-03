#/usr/bin/perl

package Braid;

use vars qw();

sub deltaBraid($)
{
  my ($n) = @_;
  my @crossings = ( );
  if ($n < 0)
  {
    unshift(@crossings,deltaBraid($n+1));
    for (my $i = $n+1; $i < 0; $i++)
    {
      unshift(@crossings,$i);
    }
  }
  elsif ($n > 0)
  {
    push(@crossings,deltaBraid($n-1));
    for (my $i = $n-1; $i > 0; $i--)
    {
      push(@crossings,$i);
    }
  }
  return @crossings;
}

# Constructor
sub new
{
  my (undef,$width,@word) = @_;
  my $self = { };
  bless($self);
  $self->{"width"} = abs($width);
  foreach my $x (@word)
  {
    $self->{"width"} = abs($x)+1 if (abs($x) >= $self->{"width"});
  }
  my @nword = ( );
  my $w = $self->{"width"};
  foreach my $x (@word)
  {
    if ($x =~ /^\s*-D(\d*)\s*$/i)
    {
      push(@nword, ($1 ? deltaBraid(-$1) : deltaBraid(-$w)));
    }
    elsif ($x =~ /^\s*D(\d*)\s*$/i)
    {
      push(@nword, ($1 ? deltaBraid($1) : deltaBraid($w)));
    }
    else
    {
      push(@nword,$x);
    }
  }
  $self->{"word"} = [ @nword ];
  return $self;
}

# Return copy of braid
sub copy($)
{
  my ($self) = @_;
  return new Braid($self->width(),$self->toList());
}

# Width (number of strings) of braid
sub width($)
{
  my ($self) = @_;
  return $self->{"width"};
}

# Length (number of crossings) of braid
sub length($)
{
  my ($self) = @_;
  my @word = $self->toList();
  return scalar(@word);
}

# Format as TeX string
sub toTeX($)
{
  my ($self) = @_;
  my $str = "";
  foreach $x ($self->toList())
  {
    next if ($x == 0);
    my ($i,$e) = (abs($x),($x < 0 ? -1 : 1));
    $str .= "\\sigma_{" . abs($x) . "}" . ($x < 0 ? "^{-1} " : " ");
  }
  $str =~ s/\s*$//;
  return $str;
}

# Return list of crossings
sub toList($)
{
  my ($self) = @_;
  return @{$self->{"word"}};
}

# Format as comma-separated list
sub toString($)
{
  my ($self) = @_;
  return "(" . join(",",$self->toList()) . ")";
}

# Do Reidemeister-2 reductions (cancellations) if possible
sub reduceR2($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my @nword = ( );
  foreach $x (@word)
  {
    if (scalar(@nword) == 0)
    {
      push(@nword,$x);
    }
    elsif ($nword[-1] == -$x)
    {
      pop(@nword);
    }
    else
    {
      push(@nword,$x);
    }
  }
  $self->{"word"} = [ @nword ];
}

# Do Markov-1 (conjugacy) reductions if possible
sub reduceM1($)
{
  my ($self) = @_;
  my @word = $self->toList();
  while (scalar(@word) > 0)
  {
    last if ($word[0] != -$word[-1]);
    pop(@word);
    shift(@word);
  }
  $self->{"word"} = [ @word ];
}

# Do Markov-2 reductions if possible
sub reduceM2($)
{
  my ($self) = @_;
  my $n = $self->width();
  do
  {
    $self->reduceM2a();
    $self->reduceM2b();
  }
  while (($n > $self->width()) && ($n = $self->width()));
}

# Do Markov-2 reductions on leftmost strands if possible
sub reduceM2a($)
{
  my ($self) = @_;
  my $n = $self->width();
  my $min = $n+1;
  my $count = 0;
  my @word = $self->toList();
  my @nword = ( );
  foreach my $x (@word)
  {
    if (abs($x) < $min)
    {
      $min = abs($x);
      $count = 1;
    }
    elsif (abs($x) == $min)
    {
      $count++;
    }
  }
  return if ($count != 1);
  foreach my $x (@word)
  {
    push(@nword,($x < 0 ? $x+1 : $x-1)) if (abs($x) != $min);
  }
  $self->{"word"} = [ @nword ];
  $self->{"width"}--;
}

# Do Markov-2 reductions on rightmost strands if possible
sub reduceM2b($)
{
  my ($self) = @_;
  my $n = $self->width();
  my $max = 0;
  my $count = 0;
  my @word = $self->toList();
  my @nword = ( );
  foreach my $x (@word)
  {
    if (abs($x) > $max)
    {
      $max = abs($x);
      $count = 1;
    }
    elsif (abs($x) == $max)
    {
      $count++;
    }
  }
  return if ($count != 1);
  foreach my $x (@word)
  {
    push(@nword,$x) if (abs($x) != $max);
  }
  $self->{"word"} = [ @nword ];
  $self->{"width"}--;
}

# Delete numbered crossing from braid word
sub deleteCrossing($$)
{
  my ($self,$pos) = @_;
  my $last = $self->length()-1;
  return if ($pos > $last || $pos < 0);
  my @word = $self->toList();
  if ($pos == 0)
  {
    shift @word;
  }
  elsif ($pos == $last)
  {
    pop @word;
  }
  else
  {
    @word = (@word[(0)..($pos-1),($pos+1)..(-1)]);
  }
  $self->{"word"} = [ @word ];
}

# Change sign of numbered crossing
sub changeCrossing($$)
{
  my ($self,$pos) = @_;
  return if ($pos > $self->length()-1);
  $self->{"word"}->[$pos] *= -1;
}

sub cycle($$)
{
  my ($self,$dir) = @_;
  return if ($dir == 0 || $self->length() == 0);
  my @word = $self->toList();
  if ($dir < 0)
  {
    push(@word,shift(@word));
  }
  else
  {
    unshift(@word,pop(@word));
  }
  $self->{"word"} = [ @word ];
}

sub canR2($$)
{
  my ($self,$pos) = @_;
  my $n = $self->length();
  my @word = $self->toList();
  my ($a,$b) = @word[($pos), ($pos+1) % $n];
  return ($a == -$a);
}

sub findR2($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my $n = $self->length();
  my @positions = ( );

  for (my $i = 0; $i < $n-1; $i++)
  {
    push (@positions,$i) if $self->canR2($i);
  }
  return @positions;
}

sub transformR2($$)
{
  my ($self,$pos) = @_;
  return if (!$self->canR2($pos));
  my $n = $self->length();
  my @word = $self->toList();
  if (@word == 2)
  {
    @nword = ( );
  }
  elsif ($pos == 0)
  {
    @nword = @word[2..$n-1];
  }
  elsif ($pos == $n-2)
  {
    @nword = @word[0..$n-3];
  }
  else
  {
    @nword = @word[0..($pos-1),($pos+2)..$n-1];
  }
  $self->{"word"} = [ @nword ];
}

# Check whether we can do a Reidemeister-3 move at this position
sub canR3($$)
{
  my ($self,$pos) = @_;
  my $n = $self->length();
  my @word = $self->toList();
  my ($a,$b,$c) = @word[($pos), ($pos+1) % $n, ($pos+2) % $n];
  return ($a == $c) && (abs($a - $b) == 1);
}

# Find all possible Reidemeister-3 moves in this braid
sub findR3($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my $n = $self->length();
  my @positions = ( );

  for (my $i = 0; $i < $n-2; $i++)
  {
    push (@positions,$i) if $self->canR3($i);
  }
  return @positions;
}

# Perform Reidemeister-3 move at this position
sub transformR3($$)
{
  my ($self,$pos) = @_;
  return if (!$self->canR3($pos));
  my $n = $self->length();
  my @word = $self->toList();
  my ($a,$b,$c) = @word[($pos), ($pos+1) % $n, ($pos+2) % $n];
  @word[($pos), ($pos+1) % $n, ($pos+2) % $n] = ($b,$a,$b);
  $self->{"word"} = [ @word ];
}

sub sign($)
{
  my ($n) = @_;
  return 0 if ($n == 0);
  return ($n < 0 ? -1 : 1);
}

sub findFlipR3($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my $n = $self->length();
  my @positions = ( );

  for (my $i = 0; $i < $n; $i++)
  {
    my ($a,$b,$c) = @word[($i), ($i+1) % $n, ($i+2) % $n];
    if (abs($a) == abs($c) & abs(abs($a)-abs($b)) == 1)
    {
      if (sign($a) != sign($b) && sign($a) != sign($c))
      {
	push(@positions,[($i,$i)])
      }
      elsif (sign($b) != sign($c) && sign($b) != sign($a))
      {
	push(@positions,[($i,($i+1) % $n)])
      }
      elsif (sign($c) != sign($a) && sign($c) != sign($b))
      {
	push(@positions,[($i,($i+2) % $n)])
      }
    }
  }
  return @positions;
}

# Check whether we can do a slide move at this position
sub canSlide($$)
{
  my ($self,$pos) = @_;
  my $l = $self->length();
  my $w = $self->width();
  return 0 if ($w < 3 || $l < 2 || $pos > $n-1 || $pos < 0);
  my @word = $self->toList();
  my ($a,$b) = @word[$pos,$pos+1];
  return (abs($a-$b) > 1);
}

# Find all possible slide moves in this braid
sub findSlide($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my $n = $self->length();
  my @positions = ( );

  for (my $i = 0; $i < $n-1; $i++)
  {
    push (@positions,$i) if $self->canSlide($i);
  }
  return @positions;
}

sub transformSlide($$)
{
  my ($self,$pos) = @_;
  return if (!$self->canSlide($pos));
  my @word = $self->toList();
  my ($a,$b) = @word[$pos,$pos+1];
  @word[$pos,$pos+1] = ($b,$a);
  $self->{"word"} = [ @word ];
}

sub findAlliteration($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my $n = $self->length();
  my @positions = ( );

  for (my $i = 0; $i < $n; $i++)
  {
    push(@positions,$i) if ($word[$i] == $word[($i+1) % $n]);
  }
  return @positions;
}

sub canFlipM1($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my $n = $self->length();
  return 0 if ($n < 2);
  return 1 if ($word[0] == $word[-1]);
  return 0;
}

sub findGoodFlip($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my $n = $self->length();
  my @strands = (0) x $self->width();
  my @crossings = (0) x $self->length();
  my $strand = 0;
  my $pos = 0;
  my @positions = ( );
  my $unseen = $self->width() - 1;

  while ($unseen > 0)
  {
    #print "strand: $strand\nunseen: $unseen\n";
    $strands[$strand] = 1;
    for ($pos = 0; $pos < $self->length(); $pos++)
    {
      #print "  pos: $pos\n    crossing: " . $word[$pos] . "\n";
      #print "    strand: $strand";
      if (abs($word[$pos]) == $strand + 1) # if we're at the left-hand strand
      {
	#print " -> " . ($strand + 1) . "\n";
	if ($crossings[$pos] == 0) # if this crossing is unseen
	{
	  push(@positions,$pos) if ($word[$pos] < 0);
	  $crossings[$pos] = 1;
	}
	$strand++;
      }
      elsif (abs($word[$pos]) == $strand) # if we're at the right-hand strand
      {
	#print " -> " . ($strand - 1) . "\n";
	if ($crossings[$pos] == 0) # if this crossing is unseen
	{
	  push(@positions,$pos) if ($word[$pos] > 0);
	  $crossings[$pos] = 1;
	}
	$strand--;
      }
      else
      {
	#print "\n";
      }
    }
    #print "  strand: $strand (" . ("unseen","seen")[$strands[$strand]] . ")\n";
    if ($strands[$strand] == 0)
    {
      $unseen--;
    }
    elsif ($unseen > 0)
    {
      for ($strand = 0; $strand < $self->width(); $strand++)
      {
	next if ($strands[$strand] == 1);
	last;
      }
    }
    #print "\n";
  }
  return @positions;
}

1;
