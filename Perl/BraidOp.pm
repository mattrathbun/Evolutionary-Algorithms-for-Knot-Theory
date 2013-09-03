#!/usr/bin/perl

package BraidOp;

use Braid;

use vars qw(@opnames);

# @opnames = qw(R2 S U M1 M2 R3 FR2 FR3 FM1 C);
@opnames = qw(R2 S U M2 R3 C);

sub randomOp()
{
  my $op;
  do
  {
    $op = new BraidOp($opnames[int(rand(@opnames))]);
  }
  while (!defined $op);
  return $op;
}

# Constructor
sub new
{
  my (undef,$str) = @_;
  my $self = { };
  bless($self);
  $self->{"str"} = $str;
  return $self;
}

sub copy($)
{
  my ($self) = @_;
  return new BraidOp($self->toString());
}

sub toString($)
{
  my ($self) = @_;
  return $self->{"str"};
}

sub toTeX($)
{
  my ($self) = @_;
  my $str = $self->{"str"};
  $str =~ s/^([[:alpha:]]+)/\\mathit{$1}/;
  $str =~ s/(\d)/_{$1}/;
  return $str;
}

sub apply($$)
{
  my ($self,$braid) = @_;
  my $str = uc($self->{"str"});
  my $flips = 0;
  my $effect = 0;
  if ($str eq "R2")
  {
    my $l = $braid->length();
    $braid->reduceOneR2();
    $effect = 1 if ($braid->length() < $l);
  }
  elsif ($str eq "S")
  {
    my @pos = $braid->findSlide();
    if (scalar(@pos))
    {
      $braid->transformSlide($pos[0]);
      $effect = 1;
    }
  }
  elsif ($str eq "U")
  {
    $braid->changeCrossing(0);
    $flips++;
    $effect = 1;
  }
  elsif ($str eq "M1")
  {
    my $l = $braid->length();
    $braid->reduceM1();
    $effect = 1 if ($braid->length() < $l);
  }
  elsif ($str eq "M2")
  {
    my $l = $braid->length();
    $braid->reduceM2();
    $effect = 1 if ($braid->length() < $l);
  }
  elsif ($str eq "R3")
  {
    my @pos = $braid->findR3();
    if (scalar(@pos))
    {
      $braid->transformR3($pos[0]);
      $effect = 1;
    }
  }
  elsif ($str eq "FR2")
  {
    my @pos = $braid->findAlliteration();
    if (scalar(@pos))
    {
      $braid->changeCrossing($pos[0]);
      $braid->transformR2($pos[0]);
      $flips++;
      $effect = 1;
    }
  }
  elsif ($str eq "FR3")
  {
    my @pos = $braid->findFlipR3();
    if (scalar(@pos))
    {
      $braid->changeCrossing($pos[0]->[1]);
      $braid->transformR3($pos[0]->[0]);
      $flips++;
      $effect = 1;
    }
  }
  elsif ($str eq "FM1")
  {
    if ($braid->canFlipM1())
    {
      $braid->changeCrossing(0);
      $braid->reduceM1();
      $flips++;
      $effect = 1;
    }
  }
  elsif ($str eq "C")
  {
    $braid->cycle(-1);
    $effect = 1;
  }
  elsif ($str eq "G")
  {
    my @pos = $braid->findGoodFlip();
    if (scalar(@pos))
    {
      $braid->changeCrossing($pos[0]);
      $flips++;
      $effect = 1;
    }
  }
  return (wantarray ? ($flips,$effect) : $flips);
}

sub isFlip($)
{
  my ($self) = @_;
  return ($self->toString() =~ /^[FG]/);
}

sub isReduction($)
{
  my ($self) = @_;
  my $str = $self->toString();
  return ($str eq "R2" ||
    $str eq "M1" ||
    $str eq "M2" ||
    $str eq "FR2" ||
    $str eq "FM1");
}

1;
