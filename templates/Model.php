<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class {{class}} extends Model
{
    use HasFactory;

    protected $table = '{{table}}';

    protected $guarded = [ {{#cg}}  guarded {{/cg}} ];

}
