import 'dart:async';
import 'package:first/screens/stops_screen.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/stop_info.dart';
import 'subscreens/home_empty_screen.dart';
import 'subscreens/home_non_empty_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final List<StopInfo> items = [];

  String _time = "";
  String _date = "";
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _updateDateTime();
    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      _updateDateTime();
    });
  }

  void _updateDateTime() {
    final now = DateTime.now();
    setState(() {
      _time = DateFormat.Hm().format(now);
      _date = DateFormat("dd.MM.yyyy").format(now);
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final height = MediaQuery.of(context).size.height;
    final width = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: Colors.grey.shade200,
      appBar: AppBar(
        toolbarHeight: height * 0.1,
        titleSpacing: width * 0.01,
        title: Row(
          children: [
            SizedBox(width: width * 0.01),
            CircleAvatar(
              radius: 18,
              backgroundColor: Colors.grey.shade300,
              child: const Icon(Icons.person, color: Colors.black54),
            ),
            const Spacer(),
            const Text('Sixfab', style: TextStyle(fontWeight: FontWeight.w800)),
            const Spacer(),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  _time,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 2),
                Text(_date, style: const TextStyle(fontSize: 12)),
              ],
            ),
            SizedBox(width: width * 0.01),
          ],
        ),
      ),
      body: items.isEmpty
          ? const HomeEmptyScreen()
          : const HomeNonEmptyScreen(),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.indigoAccent,
        hoverColor: Colors.indigo,
        onPressed: () async {
          try {
            // ignore: unused_local_variable
            final result = await Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => StopsScreen()),
            );
          } catch (e) {
            ScaffoldMessenger.of(context,).showSnackBar(
              SnackBar(content: Text("Hata oluştu: $e")));
          }
        },
        child: const Icon(Icons.add_circle_sharp),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    );
  }
}
