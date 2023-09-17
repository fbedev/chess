# This example requires the 'message_content' privileged intents

import os
import discord
import chess

bot = discord.Bot()
games = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

chess_group = bot.create_group("chess", "Chess related commands")

@chess_group.command()
async def startgame(ctx):
    # Initialize a new chess game
    games[ctx.guild.id] = chess.Board()
    
    # Get the initial chessboard and send it as an embed
    game = games[ctx.guild.id]
    formatted_board = format_chessboard(game)
    embed = discord.Embed(title="Chess Game", color=0x00ff00)
    embed.add_field(name="Current Board:", value=f"```\n{formatted_board}\n```", inline=False)
    await ctx.respond(embed=embed)

@chess_group.command()
async def move(ctx, move_str: discord.Option(str, "Enter your move in UCI format")):
    # Make a move in the chess game
    if ctx.guild.id in games:
        game = games[ctx.guild.id]
        try:
            move = chess.Move.from_uci(move_str)
            if move in game.legal_moves:
                game.push(move)
                formatted_board = format_chessboard(game)
                embed = discord.Embed(title="Chess Game", color=0x00ff00)
                embed.add_field(name="Current Board:", value=f"```\n{formatted_board}\n```", inline=False)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond('Invalid move!')
        except ValueError:
            await ctx.respond('Invalid move format!')
    else:
        await ctx.respond('Start a new game with `/chess startgame`.')

def format_chessboard(board):
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    piece_symbols = {
        'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
        'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
    }
    
    formatted_board = "    " + "   ".join(files) + "\n   " + "--- " * 8 + "\n"
    
    for rank in ranks:
        rank_line = rank + " | "
        for file in files:
            square = file + rank
            piece = board.piece_at(chess.SQUARE_NAMES.index(square))
            if piece:
                rank_line += piece_symbols[str(piece)] + " | "
            else:
                rank_line += "  | "
        formatted_board += rank_line + "\n   " + "--- " * 8 + "\n"
    
    formatted_board += "    " + "   ".join(files)
    
    return formatted_board

async def send_chessboard(ctx, game):
    # Create an embed with the chessboard
    embed = discord.Embed(title="Chess Game", color=0x00ff00)
    formatted_board = format_chessboard(game)
    embed.add_field(name="Current Board:", value=f"```\n{formatted_board}\n```", inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ["DISCORD_TOKEN"])
