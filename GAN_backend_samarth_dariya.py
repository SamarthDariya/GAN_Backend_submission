import heapq
import csv

def read_trades_from_csv(filename):
    """
    Reads the trades from the given CSV file and returns them as a list of dictionaries.
    """
    with open(filename) as f:
        reader = csv.DictReader(f)
        return list(reader)

def main():
    trades = read_trades_from_csv("trades.csv")
    opened_trades = {}  # dictionary to store the opened trades, keyed by symbol
    realized_pnl = 0  # variable to store the cumulative realized PNL

    for trade in trades:
        symbol = trade["SYMBOL"]
        side = trade["SIDE"]
        price = float(trade["PRICE"])
        quantity = int(trade["QUANTITY"])

        if side == "B":
            # add the trade to the dictionary of opened trades
            if symbol not in opened_trades:
                opened_trades[symbol] = []
            heapq.heappush(opened_trades[symbol], (trade["TIME"], side, price, quantity))

        else:  # side == "S"
            # find the corresponding opening trade to close it
            if symbol not in opened_trades or not opened_trades[symbol]:
                # there is no opened trade for this symbol, skip this trade
                continue

            # find the oldest opened trade that has enough quantity
            while opened_trades[symbol] and opened_trades[symbol][0][3] < quantity:
                _, _, open_price, open_quantity = heapq.heappop(opened_trades[symbol])
                quantity -= open_quantity

            if not opened_trades[symbol]:
                # there are no more opened trades, skip this trade
                continue

            # we found the corresponding opened trade, compute the PNL and print it
            open_time, open_side, open_price, open_quantity = heapq.heappop(opened_trades[symbol])
            close_time = trade["TIME"]
            pnl = quantity * (price - open_price)
            print(f"{open_time},{close_time},{symbol},{quantity},{pnl},{open_side},{side},{open_price},{price}")
            realized_pnl += pnl

    # print the cumulative realized PNL
    print(realized_pnl)

if __name__ == "__main__":
    main()