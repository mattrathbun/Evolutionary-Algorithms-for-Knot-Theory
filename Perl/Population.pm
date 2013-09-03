#/usr/bin/perl

use Braid;
use BraidOp;
use BraidOpList;

package Population;

use vars qw();

# Constructor
sub new
{
  my (undef,$num,$maxl,$minl) = @_;
  my $self = { };
  bless($self);
  $self->{"oplists"} = [ ];
  $self->randomInit($num,$maxl,$minl) if ($num);
  return $self;
}

sub randomInit($;$$$)
{
  my ($self,$num,$maxl,$minl) = @_;
  #srand(time);
  #srand(time ^ $$ ^ unpack "%L*", `ps axww | gzip -f`);
  $num = ($num ? abs($num) : 20);
  my @ols = ( );
  for (my $i = 0; $i < $num; $i++)
  {
    push(@ols, BraidOpList::randomOpList($maxl,$minl));
  }
  $self->{"oplists"} = [ @ols ];
}

sub toList($)
{
  my ($self) = @_;
  return @{$self->{"oplists"}};
}

sub size($)
{
  my ($self) = @_;
  return scalar($self->toList());
}

sub iterate($$;$)
{
  my ($self,$fit,$mu) = @_;
  $mu = 0.05 if (!defined $mu);
  my $n = $self->size();
  my @pop1 = sort { &{$fit}($b) <=> &{$fit}($a) } $self->toList();
  my $tfv = 0;
  my $max = 0;
  my $min = 1000000;
  foreach my $ol (@pop1)
  {
    my $fv = &{$fit}($ol);
    $max = ($fv > $max ? $fv : $max);
    $min = ($fv < $min ? $fv : $min);
    $tfv += $fv;
  }
  my $afv = $tfv/$self->size();

  print "total fitness = $tfv\n";
  print "average fitness = $afv\n";
  print "max fitness = $max, " . ($max/$afv) . "\n";
  print "min fitness = $min, " . ($min/$afv) . "\n";

  my @pop2 = ( );
  foreach my $ol (@pop1)
  {
    my $fv = &{$fit}($ol);
    for (my $i = ($fv/$afv); $i > 0; $i--)
    {
      push(@pop2,$ol->copy()) if (rand() <= $i);
    }
  }
  for (my $i = scalar(@pop2); $i < $n; $i++)
  {
    unshift(@pop2,$pop1[0]->copy());
  }
  @pop2 = @pop2[0..($n-1)];

  for (my $i = 0; $i < scalar(@pop2) - 1; $i += 2)
  {
    # print "recombining\n";
    # print "  " . $pop2[$i]->toString() . "\n";
    # print "  " . $pop2[$i+1]->toString() . "\n";
    ($pop2[$i],$pop2[$i+1]) = $pop2[$i]->recombine($pop2[$i+1]);
  }

  for (my $i = 0; $i < scalar(@pop2); $i++)
  {
    if (rand() < $mu)
    {
      # print "mutation\n";
      # print "  " . $pop2[$i]->toString() . "\n";
      $pop2[$i]->mutate();
      # print "  " . $pop2[$i]->toString() . "\n";
    }
  }

  # print "size = " . scalar(@pop2) . "\n";
  my @pop3 = sort { &{$fit}($b) <=> &{$fit}($a) } @pop2;
  $self->{"oplists"} = [ @pop3 ];
}

1;
