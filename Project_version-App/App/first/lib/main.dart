import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() => runApp(const PTEApp());

class PTEApp extends StatelessWidget {
  const PTEApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PTE SSDMS',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.blueGrey,
        textTheme: const TextTheme(
          titleMedium: TextStyle(fontWeight: FontWeight.w700),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
