import 'package:flutter/material.dart';

class StopsScreen extends StatelessWidget {
  const StopsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            const Spacer(),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red.shade400,
                foregroundColor: Colors.black
              ),
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text("Save And Return", style: TextStyle(fontWeight: FontWeight.bold)),
            ),
            const SizedBox(height: 20)
          ],
        ),
      ),
    );
  }
}
