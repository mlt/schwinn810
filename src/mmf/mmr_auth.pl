#!/usr/bin/perl
# MapMyRun authorization prototype

use LWP::UserAgent;
use Net::OAuth;
#$Net::OAuth::PROTOCOL_VERSION = Net::OAuth::PROTOCOL_VERSION_1_0A;
use HTTP::Request::Common;
my $ua = LWP::UserAgent->new;

open FILE, glob("~/.schwinn810mmr");
$_=<FILE>;
chomp;
my $consumer_key = $_;
$_=<FILE>;
chomp;
my $consumer_secret = $_;

my $request = Net::OAuth->request("request token")->new(
							consumer_key => $consumer_key,
							consumer_secret => $consumer_secret,
							request_url => 'http://api.mapmyfitness.com/3.1/oauth/request_token',
							request_method => 'POST',
							signature_method => 'HMAC-SHA1',
							timestamp => time(),
							nonce => time()*rand()
						       );

$request->sign;

my $res = $ua->request(POST $request->to_url); # Post message to the Service Provider

if ($res->is_success) {
  my $response = Net::OAuth->response('request token')->from_post_body($res->content);
  print "Got Request Token ", $response->token, "\n";
  print "Got Request Token Secret ", $response->token_secret, "\n";
  print "Go to http://api.mapmyfitness.com/3.1/oauth/authorize?&oauth_token=" . $response->token . " and hit <enter> once authorized\n";
  <STDIN>;
  my $request = Net::OAuth->request("access token")->new(
							 consumer_key => $consumer_key,
							 consumer_secret => $consumer_secret,
							 token => $response->token,
							 token_secret => $response->token_secret,
							 signature_method => 'HMAC-SHA1',
							 request_url => 'http://api.mapmyfitness.com/3.1/oauth/access_token',
							 request_method => 'POST',
							 timestamp => time(),
							 nonce => time()*rand()
							);

  $request->sign;

  my $res = $ua->request(POST $request->to_url); # Post message to the Service Provider

  if ($res->is_success) {
    my $response = Net::OAuth->response('access token')->from_post_body($res->content);
    print "Got Access Token ", $response->token, "\n";
    print "Got Access Token Secret ", $response->token_secret, "\n";
  } else {
    die "Something went wrong 2" . $res->content;
  }

print "Append access token & secret to your .schwinn810mmr\n";
