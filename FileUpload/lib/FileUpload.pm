package FileUpload;
use Dancer ':syntax';

use Amazon::S3::Thin;

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

get '/.well-known/pki-validation/:file' => sub {
        send_file( params->{file} );
};

get '/revisar' => sub {
        my $url = 'https://www.google.com';
        
        my $response = `aws quicksight get-dashboard-embed-url --namespace default --dashboard-id 0fd6237e-e629-49d1-a4fc-005f13cdc396 --identity-type ANONYMOUS --aws-account-id 463668497025 --namespace default`;

        my $response_ref = from_json($response);

        if($response_ref->{Status} == 200){
                $url = $response_ref->{EmbedUrl};
        }

        return redirect $url;
        return template 'revisar', { url => $url };
};

true;
