import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';

import 'inputScreen.dart';
import 'predictionScreen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(CodexApp());
}

class CodexApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        brightness: Brightness.dark,
        accentColor: Colors.orange,
      ),
      routes: {
        '/': (context) => InputScreen(),
      },
      onGenerateRoute: (settings) {
        if (settings.name == PredictionScreen.routeName) {
          final ScreenArguments args = settings.arguments as ScreenArguments;
          return MaterialPageRoute(
            builder: (context) {
              return PredictionScreen(
                title: args.title,
                credit: args.credit,
                ingredients: args.ingredients,
                predictions: args.predictions,
              );
            },
          );
        }
        return null;
      },
    );
  }
}