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
                    aws_access_key_id => '',
                    aws_secret_access_key => '',
                    region => ''
            });
    
            my $response = $s3->head_object('hackathon-test-bbva-2021', $archivo->filename );
            if($response->code == 200){
                return template 'enviar', { duplicated_file => $archivo->filename };
            }

            my $response = $s3->put_object('hackathon-test-bbva-2021', $archivo->filename, $archivo->content, { content_type => 'text/plain'});
            if($response->is_error) {
                return template 'enviar',{ error_file => $archivo->filename };
            }
    }

    return template 'index',{ success => 1 };
};

get '/.well-known/pki-validation/:file' => sub {
        send_file( params->{file} );
};

get '/revisar' => sub {
        my $url = 'https://www.google.com';
        
        my $response = `aws quicksight get-dashboard-embed-url --namespace default --dashboard-id 14183d20-abbb-4b6e-978d-dffe8620dcbe --identity-type ANONYMOUS --aws-account-id  --namespace default`;

        my $response_ref = from_json($response);

        if($response_ref->{Status} == 200){
                $url = $response_ref->{EmbedUrl};
        }

        return redirect $url;
        return template 'revisar', { url => $url };
};

true;
