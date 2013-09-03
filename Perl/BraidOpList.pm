#!/usr/bin/perl

package BraidOpList;

use BraidOp;

use vars qw();

sub randomOpList(;$$)
{
  my ($maxl,$minl) = @_;
  $maxl = ($maxl ? abs($maxl) : 20);
  $minl = ($minl && $minl <= $maxl ? abs($minl) : $maxl);
  my $len = ($minl == $maxl ? $maxl : int(rand($maxl-$minl+1)) + $minl);
  my @ops = ( );
  for (my $i = 0; $i < $len; $i++)
  {
    push(@ops, BraidOp::randomOp());
  }
  return new BraidOpList(@ops);
}

# Constructor
sub new
{
  my (undef,@ops) = @_;
  my $self = { };
  bless($self);
  $self->{"list"} = [ @ops ];
  return $self;
}

sub copy
{
  my ($self) = @_;
  my @ol = ( );
  foreach my $op ($self->toList())
  {
    push(@ol,$op->copy()) if (defined $op);
  }
  return new BraidOpList(@ol);
}

sub toString($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my @str = ( );
  foreach my $op (@word)
  {
    push(@str,$op->toString()) if (defined $op);
  }
  return join(" ", @str);
}

sub toTeX($)
{
  my ($self) = @_;
  my @word = $self->toList();
  my @str = ( );
  foreach my $op (@word)
  {
    push(@str,$op->toTeX());
  }
  return join("\\,", @str);
}

sub length($)
{
  my ($self) = @_;
  return scalar($self->toList());
}

sub toList($)
{
  my ($self) = @_;
  return @{$self->{"list"}};
}

sub apply($$)
{
  my ($self,$braid) = @_;
  my $b = $braid->copy();
  my $flips = 0;
  my $nl = new BraidOpList();
  foreach my $op ($self->toList())
  {
    if (defined $op)
    {
      my ($fl,$ef) = $op->apply($b);
      $flips += $fl;
      $nl->append($op) if ($ef);
    }
    # print "    " . $op->toString() . " = " . $b->toString() . "\n";
  }
  return (wantarray ? ($b, $flips, $nl) : $b);
}

sub append($@)
{
  my ($self,@ops) = @_;
  my @cur = $self->toList();
  $self->{"list"} = [ @cur, @ops ];
}

sub prepend($@)
{
  my ($self,@ops) = @_;
  my @cur = $self->toList();
  $self->{"list"} = [ @ops, @cur ];
}

sub mutate($)
{
  my ($self) = @_;
  my $n = $self->length();
  my $type = int(rand(3));
  my @ol = $self->toList();
  if ($type == 0) # randomise
  {
    $ol[int(rand($n))] = BraidOp::randomOp();
  }
  elsif ($type == 1) # cyclic permutation
  {
    push(@ol, shift @ol);
  }
  elsif ($type == 2) # cyclic permutation
  {
    unshift(@ol, pop @ol);
  }
  elsif ($type == 3) # delete random operation
  {
    $pos = int(rand($n));
    splice(@ol,$pos);
  }
  elsif ($type == 4) # insert random operation
  {
    $pos = int(rand($n));
    $ol = BraidOp::randomOp();
    @ol = (@ol[0..$pos],$ol,@ol[($pos+1)..$#ol]);
  }
  $self->{"list"} = [ @ol ];
}

sub recombine($$)
{
  my ($self,$other) = @_;
  my $sn = $self->length();
  my @sword = $self->toList();
  my $on = $other->length();
  my @oword = $other->toList();
  my $pos = int(rand($sn < $on ? $sn : $on));
  my @snword = (@sword[0..$pos], @oword[($pos+1)..$on-1]);
  my @onword = (@oword[0..$pos], @sword[($pos+1)..$sn-1]);
  return (new BraidOpList(@snword), new BraidOpList(@onword));
}

sub flipCount($)
{
  my ($self) = @_;
  my $fc = 0;
  foreach my $op ($self->toList())
  {
    $fc++ if ($op->isFlip());
  }
  return $fc;
}

sub reductionCount($)
{
  my ($self) = @_;
  my $rc = 0;
  foreach my $op ($self->toList())
  {
    $rc++ if ($op->isReduction());
  }
  return $rc;
}

1;
