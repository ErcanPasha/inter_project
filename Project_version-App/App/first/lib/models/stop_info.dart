class StopInfo {
  final String name;
  final String side; // Yaka
  final String district; // İlçe
  final String lastUpdate; // Son Güncelleme
  final List<PassengerPoint> passengerSeries; // Yolcu Bilgisi
  final List<String> incomingBuses; // Gelen Otobüsler

  const StopInfo({
    required this.name,
    required this.side,
    required this.district,
    required this.lastUpdate,
    this.passengerSeries = const [],
    this.incomingBuses = const [],
  });
}

class PassengerPoint {
  final String time; // "12:32"
  final int count;
  const PassengerPoint(this.time, this.count);
}
