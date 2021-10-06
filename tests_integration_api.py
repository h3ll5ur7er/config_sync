from swagger_client import DefaultApi


if __name__ == '__main__':
    client = DefaultApi()
    client.api_client.configuration.host = "http://localhost:8000"

    client.setup()
    data0 = client.serialize()
    values0 = client.get_all_values()
    hash0 = client.get_hash()

    client.delete_entry("c")

    data1 = client.serialize()
    values1 = client.get_all_values()
    hash1 = client.get_hash()

    client.compress("1fa81afda2bdf9f499348a1f2673dce0")

    data2 = client.serialize()
    values2 = client.get_all_values()
    hash2 = client.get_hash()

    client.load(data0)

    data3 = client.serialize()
    values3 = client.get_all_values()
    hash3 = client.get_hash()

    print(data0)
    print("-"*20)
    print(data1)
    print("-"*20)
    print(data2)
    print("-"*20)
    print(data3)
    print("="*20)
    print("="*20)
    print(values0)
    print("-"*20)
    print(values1)
    print("-"*20)
    print(values2)
    print("-"*20)
    print(values3)
    print("="*20)
    print("="*20)
    print(hash0)
    print("-"*20)
    print(hash1)
    print("-"*20)
    print(hash2)
    print("-"*20)
    print(hash3)
    print("="*20)
    print("="*20)
