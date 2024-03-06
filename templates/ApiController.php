<?php

namespace App\Http\Controllers\api;

use App\Http\Controllers\Controller;
use App\Models\Board;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;

/**
 * Class BoardController
 * @package App\Http\Controllers\api
 */
class BoardController extends Controller
{
    //

    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        Log::Debug('BoardController@index');

        $boards = Board::all(); // SELECT * FROM boards

        $data = [
            'status' => 200,
            'boards' => $boards,
        ];

        return response()->json($data, 200);
    }

    /**
     * Display the specified resource.
     */
    public function show($id)
    {
        Log::Debug("BoardController@show $id");

        $board = Board::find($id); // SELECT * FROM boards WHERE id = $id

        if (!$board) {
            // 404 Not Found
            $data = [
                'status' => 404,
                'message' => 'Board not found',
            ];

            return response()->json($data, 404);
        }

        // 200 OK
        $data = [
            'status' => 200,
            'board' => $board,
        ];

        return response()->json($data, 200);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        Log::Debug('BoardController@store');

        $validator = Validator::make($request->all(), [
            'name' => 'required|string|max:255',
            'description' => '',
            'email' => 'email|required',
            'favorite' => 'required|boolean',
            'read_at' => 'date',
            'href' => '',
            'image' => '',
            'theme' => 'in:light,dark',
        ]);

        if ($validator->fails()) {
            $data = [
                'status' => 422,
                'errors' => $validator->errors(),
                'message' => 'Validation failed',
            ];
            Log::Debug('BoardController@store validation failed', $data);

            return response()->json($data, 422);
        }

        $board = new Board;
        $board->name = $request->name;
        $board->description = $request->description;
        $board->email = $request->email;
        $board->favorite = $request->favorite;
        $board->read_at = $request->read_at;
        $board->href = $request->href;
        $board->image = $request->image;
        $board->theme = $request->theme;

        $board->save();

        $data = [
            'status' => 200,
            'board' => $board,
        ];
        Log::Debug('BoardController@store saved in database', $data);
        return response()->json($data, 200);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, int $id)
    {
        Log::Debug("BoardController@update $id");

        $validator = Validator::make($request->all(), [
            'name' => 'string|max:255',
            'description' => '',
            'email' => 'email',
            'favorite' => 'boolean',
            'read_at' => 'date',
            'href' => '',
            'image' => '',
            'theme' => 'in:light,dark',
        ]);

        if ($validator->fails()) {
            $data = [
                'status' => 422,
                'errors' => $validator->errors(),
                'message' => 'Validation failed',
            ];
            Log::Debug('BoardController@store validation failed', $data);

            return response()->json($data, 422);
        }

        $board = Board::find($id);

        if (!$board) {
            $data = [
                'status' => 404,
                'message' => 'Board not found',
            ];

            return response()->json($data, 404);
        }

        $board->name = $request->name;
        $board->description = $request->description;
        $board->email = $request->email;
        $board->favorite = $request->favorite;
        $board->read_at = $request->read_at;
        $board->href = $request->href;
        $board->image = $request->image;
        $board->theme = $request->theme;
        $board->save();

        $data = [
            'status' => 200,
            'board' => $board,
        ];

        return response()->json($data, 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id)
    {
        Log::Debug("BoardController@delete $id");

        $board = Board::find($id);

        if (!$board) {
            $data = [
                'status' => 404,
                'message' => 'Board not found',
            ];

            return response()->json($data, 404);
        }

        $board->delete();

        $data = [
            'status' => 200,
            'message' => "Board $id deleted",
        ];

        return response()->json($data, 200);
    }
}
