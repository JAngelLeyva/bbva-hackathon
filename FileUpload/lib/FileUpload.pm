package FileUpload;
use Dancer ':syntax';

use Amazon::S3;

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
            my $s3 = Amazon::S3->new({
                    aws_secret_key_id => 'AKIAWX5GLZKAQIFDZJCM',
                    aws_secret_access_key => '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',
                    retry => 1
            });

            my $bucket =  $s3->bucket('hackathon-test-bbva-2021');
            $bucket->add_key(time, $archivo->content, { content_type => 'text/plain'});
    }

    return template 'enviar';
};


true;
