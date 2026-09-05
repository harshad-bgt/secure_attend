import os

path = r'E:\SecureAttend\apk_build\lib\core\api_client.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

put_method = '''
  static Future<http.Response> put(String endpoint, {Map<String, dynamic>? data}) async {
    final headers = await _getHeaders();
    final baseUrl = await getBaseUrl();
    final response = await http.put(
      Uri.parse('\\'),
      headers: headers,
      body: data != null ? jsonEncode(data) : null,
    ).timeout(const Duration(seconds: 10));
    return response;
  }
'''

if 'static Future<http.Response> put' not in content:
    content = content.replace('static Future<http.Response> postMultipart', put_method + '\n  static Future<http.Response> postMultipart')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
