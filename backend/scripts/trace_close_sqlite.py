"""
Trace and (optionally) close live sqlite3.Connection objects.
Run this after tests to find who holds DB connections and try to close them safely.
"""
import gc
import sqlite3
import sys

print('Scanning for sqlite3.Connection objects...')
found = []
for obj in gc.get_objects():
    try:
        if isinstance(obj, sqlite3.Connection):
            found.append(obj)
    except Exception:
        continue

if not found:
    print('No sqlite3.Connection objects found.')
    sys.exit(0)

print(f'Found {len(found)} sqlite3.Connection object(s).')
for i, conn in enumerate(found, 1):
    try:
        print(f'\n--- Connection #{i} ---')
        print('repr:', repr(conn))
        # show if it's closed
        try:
            # sqlite3 connection has attribute 'in_transaction' in Python3.8+, use it carefully
            state = getattr(conn, 'in_transaction', 'N/A')
            print('in_transaction:', state)
        except Exception:
            pass
        # list referrers (limited)
        referrers = gc.get_referrers(conn)
        print(f'Referrers (top {min(10, len(referrers))}):')
        for j, ref in enumerate(referrers[:10], 1):
            try:
                t = type(ref)
                s = repr(ref)
                if len(s) > 200:
                    s = s[:200] + '...'
                print(f'  {j}. type={t}, repr={s}')
            except Exception:
                print(f'  {j}. <unprintable ref>')

        # Attempt to close the connection safely
        try:
            print('Attempting to close the connection...')
            conn.close()
            print('Closed successfully.')
        except Exception as e:
            print('Close failed:', repr(e))
    except Exception as e:
        print('Error inspecting connection:', repr(e))

print('\nDone scanning/closing.')
