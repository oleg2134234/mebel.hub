#!/usr/bin/perl
# Крошечный статический файловый сервер для локального предпросмотра.
#   perl tools/serve.pl <корень> <порт>
# По умолчанию: корень ".", порт 8791.
#
# Форк на соединение + таймаут на чтение запроса. Браузер открывает десятки
# параллельных соединений под галерею — одиночный блокирующий цикл на этом
# захлёбывается, поэтому каждое соединение обслуживает отдельный процесс.
use strict;
use warnings;
use IO::Socket::INET;
use POSIX ();

my $root = $ARGV[0] || '.';
my $port = $ARGV[1] || 8791;
$| = 1;

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
    woff2 => 'font/woff2',
    ttf  => 'font/ttf',
    txt  => 'text/plain; charset=utf-8',
);

my $server = IO::Socket::INET->new(
    LocalHost => '127.0.0.1',
    LocalPort => $port,
    Proto     => 'tcp',
    Listen    => 256,
    ReuseAddr => 1,
) or die "Не удалось занять порт $port: $!\n";

# подчищаем завершившиеся дочерние процессы, не блокируясь
$SIG{CHLD} = sub { while (waitpid(-1, POSIX::WNOHANG()) > 0) { } };

print "Статический сервер '$root' на http://localhost:$port\n";

while (1) {
    my $client = $server->accept or next;   # accept может прерваться сигналом CHLD
    my $pid = fork();
    if (!defined $pid) {
        # форк не удался — обслужим прямо здесь, чтобы не терять запрос
        handle($client);
        close $client;
        next;
    }
    if ($pid) { close $client; next; }       # родитель — слушаем дальше

    close $server;                            # дочерний процесс
    handle($client);
    close $client;
    exit 0;
}

sub handle {
    my ($client) = @_;
    $client->autoflush(1);
    eval {
        local $SIG{ALRM} = sub { die "timeout\n" };
        alarm 10;

        my $req = '';
        while (my $line = <$client>) {
            $req .= $line;
            last if $line =~ /^\r?\n$/;
            last if length($req) > 16384;
        }
        alarm 0;

        my ($method, $uri) = $req =~ m{^(\S+)\s+(\S+)\s+HTTP}i;
        return unless defined $method;

        if ($method !~ /^(GET|HEAD)$/i) {
            send_simple($client, 405, 'Method Not Allowed');
            return;
        }

        $uri =~ s/\?.*$//;
        $uri =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/ge;
        $uri = '/index.html' if $uri eq '/';

        my @parts = grep { length && $_ ne '.' && $_ ne '..' } split m{/}, $uri;
        my $path = "$root/" . join('/', @parts);
        $path .= '/index.html' if -d $path;

        if (-f $path && open(my $fh, '<:raw', $path)) {
            local $/;
            my $body = <$fh>;
            close $fh;
            my ($ext) = $path =~ /\.([^.\/]+)$/;
            my $type = $MIME{ lc($ext // '') } || 'application/octet-stream';
            print $client "HTTP/1.1 200 OK\r\n";
            print $client "Content-Type: $type\r\n";
            print $client "Content-Length: " . length($body) . "\r\n";
            print $client "Cache-Control: no-cache\r\n";
            print $client "Connection: close\r\n\r\n";
            print $client $body unless $method =~ /^HEAD$/i;
        }
        else {
            send_simple($client, 404, "Not Found: $uri");
        }
    };
    alarm 0;
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
