Under development<br/>

All modules development using odoo v.9c :<br/>
last commit 14bd6dd277bd5d70a716a7723290de45d76b03ab<br/>
Author: qsm-odoo <qsm@odoo.com><br/>
Date:   Wed Sep 27 16:12:36 2017 +0200<br/>

    [FIX] web: traceback on line graphs with only one data
    
    Graph tooltip destruction was fixed with commit https://github.com/odoo/odoo/commit/86252428846607cd5f4b18cef8de49a8cd0b151a#diff-5de06eee7a2eeae066aa1348a1528fe9L100.
    Unfortunately, the commit supposed that the 'display_' methods always
    returned a graph, which is wrong.
    
    opw-773759


<bold>Modules</bold>
<table>
    <thead>
        <td>No.</td>
        <td>Modul</td>
        <td>Fungsi</td>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>data_approval</td>
            <td>Modul ini merupakan master modul approval. Setelah modul ini diinstall pembuatan kontak dapat diatur melalui beberapa approval dari user-user yang berwenang. Contoh kasus setiap department pada perusahaan memiliki kepentingan pada data customer atau vendor jadi dalam pembuatan kontak dapat dipastikan user-user terkait sudah mengecek customer atau vendor sebelum data aktif pada odoo.</td>
        </tr>
    </tbody>
</table>
