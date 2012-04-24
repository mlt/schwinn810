#!/usr/bin/perl
# MapMyRun uploader prototype

use LWP::UserAgent;
use Net::OAuth;
use JSON;
use Data::Dumper;
use HTTP::Request::Common;
my $ua = LWP::UserAgent->new();

my $name = shift; # track name
my $fname = shift; # TCX to upload

open FILE, glob("~/.schwinn810mmr");
$_=<FILE>;
chomp;
my $consumer_key = $_;
$_=<FILE>;
chomp;
my $consumer_secret = $_;
$_=<FILE>;
chomp;
my $token = $_;
$_=<FILE>;
chomp;
my $token_secret = $_;

my $request = Net::OAuth->request("protected resource")->new(
							     consumer_key => $consumer_key,
							     consumer_secret => $consumer_secret,
							     token => $token,
							     token_secret => $token_secret,
							     signature_method => 'HMAC-SHA1',
							     request_url => 'http://api.mapmyfitness.com/3.1/users/authenticate_user',
							     request_method => 'POST',
							     timestamp => time(),
							     nonce => time()*rand()
							    );

$request->sign;

my $res = $ua->request(POST $request->to_url); # Post message to the Service Provider

if ($res->is_success) {
  my $data = decode_json $res->content;
  my $output = $data->{result}{output};
  print "user_id: " . $output->{user_id} . "\n";
} else {
  die "[authenticate_user] Something went wrong 1 " . $res->content;
}

open FILE, $fname;
$file_contents = do { local $/; <FILE> };
print "about to send " . length($file_contents) . " bytes\n";
my $import_tcx = 'http://api.mapmyfitness.com/3.1/workouts/import_tcx';

my $request = Net::OAuth->request("protected resource")->new(
							     consumer_key => $consumer_key,
							     consumer_secret => $consumer_secret,
							     token => $token,
							     token_secret => $token_secret,
							     signature_method => 'HMAC-SHA1',
							     request_url => 'http://api.mapmyfitness.com/3.1/workouts/import_tcx',
							     request_method => 'POST',
							     timestamp => time(),
							     nonce => time()*rand(),
							     extra_params => {
									      o => 'json',
									      tcx => $file_contents,
									      baretcx => 1,
									      name => $name
									     }
							    );

$request->sign;

my $res = $ua->post($import_tcx, $request->to_hash);

if ($res->is_success) {
} else {
  die "[write_tcx] Something went wrong 3 " . $res->message . " code=" . $res->code;
}

exit;

my $data = decode_json $res->content;
#print Dumper($data);
$workout_id = $data->{result}{output}{result}{workout_id};
$workout_key = $data->{result}{output}{result}{workout_key};
$route_id = $data->{result}{output}{result}{route_id};
$route_key = $data->{result}{output}{result}{route_key};
print "workout_id " . $workout_id . "\n";

my $request = Net::OAuth->request("protected resource")->new(
							     consumer_key => $consumer_key,
							     consumer_secret => $consumer_secret,
							     token => $token,
							     token_secret => $token_secret,
							     signature_method => 'HMAC-SHA1',
							     request_url => 'http://api.mapmyfitness.com/3.1/workouts/edit_workout',
							     request_method => 'POST',
							     timestamp => time(),
							     nonce => time()*rand(),
							     extra_params => {
									      workout_key => $workout_key,
									      workout_id => $workout_id,
									      calories_burned => 123,
									      workout_type_id => 2
#									      source => "Schwinn 810 uploader"
									     }
							    );

$request->sign;

#my $res = $ua->request(PUT $request->to_url); # Post message to the Service Provider
my $res = $ua->request(POST $request->to_url);#, Contents => $file_contents); # Post message to the Service Provider

if ($res->is_success) {
  print $res->content;
  #      my $data = decode_json $res->content;
  #      print Dumper($data);


} else {
#  my $data = decode_json $res->content;
#  print Dumper($data->{error});
#  print Dumper($res);
  die "[write_tcx] Something went wrong 3" . $res->content . " code=" . $res->code;
}
