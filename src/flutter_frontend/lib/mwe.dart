import 'dart:developer';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> main() async {
    final response = await http.post(
        Uri.https(
            //'jsonplaceholder.typicode.com', 'albums'),
                'us-central1-palates-codex.cloudfunctions.net',
                '/servePrediction'),
        headers: <String, String>{
            //'Content-Type': 'application/json; '
            //    'charset=UTF-8',
            'Content-Type': 'application/json'
        },
        body: jsonEncode(<String, String>{
            //'title': 'test',
            'ingredients': 'test',
        }),
    );
    log('response was ${response.body}');
}