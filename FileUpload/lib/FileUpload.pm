package FileUpload;
use Dancer ':syntax';

use Amazon::S3::Thin;
use Data::Dumper;

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
            my $s3 = Amazon::S3::Thin->new({
                    aws_access_key_id => 'AKIAWX5GLZKAQIFDZJCM',
                    aws_secret_access_key => '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',
                    region => 'us-east-2'

            });

            my $response = $s3->put_object('hackathon-test-bbva-2021',time.'.csv', $archivo->content, { content_type => 'text/plain'});
                    debug $response->code;
                    debug $response->as_string;
                    debug $response->is_success;
    }

    return template 'enviar';
};

get '/.well-known/pki-validation/:file' => {
        send_file( params->{file} );
};

true;
