#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket::INET;
use IO::Select;

my $root = $ARGV[0] || '.';
my $port = $ARGV[1] || 8791;

my %MIME = (
    html => 'text/html; charset=utf-8',
    htm  => 'text/html; charset=utf-8',
    js   => 'application/javascript; charset=utf-8',
    mjs  => 'application/javascript; charset=utf-8',
    css  => 'text/css; charset=utf-8',
    json => 'application/json; charset=utf-8',
    svg  => 'image/svg+xml',
    jpg  => 'image/jpeg',
    jpeg => 'image/jpeg',
    png  => 'image/png',
    webp => 'image/webp',
    gif  => 'image/gif',
    ico  => 'image/x-icon',
    mp4  => 'video/mp4',
    webm => 'video/webm',
    mov  => 'video/quicktime',
    woff => 'font/woff',
    woff2=> 'font/woff2',
    ttf  => 'font/ttf',
    txt  => 'text/plain; charset=utf-8',
);

my $server = IO::Socket::INET->new(
    LocalHost => '127.0.0.1',
    LocalPort => $port,
    Proto     => 'tcp',
    Listen    => 64,
    ReuseAddr => 1,
) or die "Cannot bind to port $port: $!\n";

$| = 1;
print "Static server for '$root' on http://localhost:$port\n";

while (my $client = $server->accept) {
    $client->autoflush(1);
    my $req = '';
    while (my $line = <$client>) {
        $req .= $line;
        last if $line =~ /^\r?\n$/;
    }
    my ($method, $uri) = $req =~ m{^(\S+)\s+(\S+)\s+HTTP}i;
    unless (defined $method) { close $client; next; }

    $uri =~ s/\?.*$//;
    $uri =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/ge;
    $uri = '/index.html' if $uri eq '/';

    # prevent path traversal
    my @parts = grep { length && $_ ne '.' && $_ ne '..' } split m{/}, $uri;
    my $path = "$root/" . join('/', @parts);

    if (-d $path) { $path .= '/index.html'; }

    if ($method !~ /^(GET|HEAD)$/i) {
        send_simple($client, 405, 'Method Not Allowed');
        close $client; next;
    }

    if (-f $path && open(my $fh, '<:raw', $path)) {
        local $/;
        my $body = <$fh>;
        close $fh;
        my ($ext) = $path =~ /\.([^.\/]+)$/;
        my $type = $MIME{lc($ext // '')} || 'application/octet-stream';
        my $len = length $body;
        print $client "HTTP/1.1 200 OK\r\n";
        print $client "Content-Type: $type\r\n";
        print $client "Content-Length: $len\r\n";
        print $client "Cache-Control: no-cache\r\n";
        print $client "Connection: close\r\n\r\n";
        print $client $body unless $method =~ /^HEAD$/i;
    } else {
        send_simple($client, 404, "Not Found: $uri");
    }
    close $client;
}

sub send_simple {
    my ($client, $code, $msg) = @_;
    my $body = "<h1>$code $msg</h1>";
    print $client "HTTP/1.1 $code $msg\r\n";
    print $client "Content-Type: text/html; charset=utf-8\r\n";
    print $client "Content-Length: " . length($body) . "\r\n";
    print $client "Connection: close\r\n\r\n";
    print $client $body;
}
