<?php

namespace App\Http\Controllers\api;

use App\Http\Controllers\Controller;
use App\Models\{{class}};
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;

/**
 * Class {{class}}Controller
 * @package App\Http\Controllers\api
 */
class {{class}}Controller extends Controller
{
    //

    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        Log::Debug('{{class}}Controller@index');

        $elements = {{class}}::all(); // SELECT * FROM {{element}}s

        $data = [
            'status' => 200,
            '{{element}}s' => $elements,
        ];

        return response()->json($data, 200);
    }

    /**
     * Display the specified resource.
     */
    public function show($id)
    {
        Log::Debug("{{class}}Controller@show $id");

        $element = {{class}}::find($id); // SELECT * FROM {{element}}s WHERE id = $id

        if (!$element) {
            // 404 Not Found
            $data = [
                'status' => 404,
                'message' => '{{class}} not found',
            ];

            return response()->json($data, 404);
        }

        // 200 OK
        $data = [
            'status' => 200,
            '{{element}}' => $element,
        ];

        return response()->json($data, 200);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        Log::Debug('{{class}}Controller@store');

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
            Log::Debug('{{class}}Controller@store validation failed', $data);

            return response()->json($data, 422);
        }

        $element = new {{class}};
        $element->name = $request->name;
        $element->description = $request->description;
        $element->email = $request->email;
        $element->favorite = $request->favorite;
        $element->read_at = $request->read_at;
        $element->href = $request->href;
        $element->image = $request->image;
        $element->theme = $request->theme;

        $element->save();

        $data = [
            'status' => 200,
            '{{element}}' => $element,
        ];
        Log::Debug('{{class}}Controller@store saved in database', $data);
        return response()->json($data, 200);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, int $id)
    {
        Log::Debug("{{class}}Controller@update $id");

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
            Log::Debug('{{class}}Controller@store validation failed', $data);

            return response()->json($data, 422);
        }

        $element = {{class}}::find($id);

        if (!$element) {
            $data = [
                'status' => 404,
                'message' => '{{class}} not found',
            ];

            return response()->json($data, 404);
        }

        $element->name = $request->name;
        $element->description = $request->description;
        $element->email = $request->email;
        $element->favorite = $request->favorite;
        $element->read_at = $request->read_at;
        $element->href = $request->href;
        $element->image = $request->image;
        $element->theme = $request->theme;
        $element->save();

        $data = [
            'status' => 200,
            '{{element}}' => $element,
        ];

        return response()->json($data, 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id)
    {
        Log::Debug("{{class}}Controller@delete $id");

        $element = {{class}}::find($id);

        if (!$element) {
            $data = [
                'status' => 404,
                'message' => '{{class}} not found',
            ];

            return response()->json($data, 404);
        }

        $element->delete();

        $data = [
            'status' => 200,
            'message' => "{{class}} $id deleted",
        ];

        return response()->json($data, 200);
    }
}
