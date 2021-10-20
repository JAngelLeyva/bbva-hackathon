package FileUpload;
use Dancer ':syntax';

our $VERSION = '0.1';

get '/' => sub {
    template 'index';
};

get '/enviar' => sub {
    template 'enviar';
};

post '/enviar' => sub {
    my @archivos = request->upload('archivo');

    foreach my $archivo (@archivos) {
            $archivo->copy_to(time . '.raw');
    }

    return template 'enviar';
};


true;
